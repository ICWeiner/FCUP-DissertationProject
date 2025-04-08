from datetime import datetime, timedelta, timezone

from ldap3 import Server, Connection, ALL, SIMPLE, SUBTREE, ANONYMOUS

import jwt
from jwt.exceptions import InvalidTokenError

from pydantic import BaseModel
from typing import Annotated
from fastapi import  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.config import settings
from app.dependencies.repositories import UserRepositoryDep

LDAP_SERVER = settings.LDAP_SERVER
LDAP_BASE_DN = settings.LDAP_BASE_DN
SECRET_KEY = settings.SECRET_KEY
ALGORITHM  = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class TokenData(BaseModel):
    username: str | None = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def ldap_authenticate(username: str, password: str) -> bool:
    # Step 1: Anonymous bind to search for the user
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, authentication=ANONYMOUS)
    conn.open()
    conn.bind()

    search_filter = f"(uid={username})"
    conn.search(search_base=LDAP_BASE_DN,
                search_filter=search_filter,
                search_scope=SUBTREE,
                )

    if not conn.entries:
        return False  # User not found

    user_dn = conn.entries[0].entry_dn

    # Step 2: Try binding as the user with the password
    user_conn = Connection(server, user=user_dn, password=password, authentication=SIMPLE)
    if user_conn.bind():
        return True
    return False

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           user_repository: UserRepositoryDep,):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = user_repository.find_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user