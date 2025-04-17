from datetime import datetime, timedelta, timezone

from ldap3 import Server, Connection, ALL, SIMPLE, SUBTREE, ANONYMOUS

import jwt

from app.dependencies.repositories import UserRepositoryDep
from app.config import settings
from app.models import UserPublic

from fastapi import  Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated, Optional, Tuple

from passlib.context import CryptContext

from logger.logger import get_logger

logger = get_logger(__name__)

LDAP_SERVER = settings.LDAP_SERVER
LDAP_BASE_DN = settings.LDAP_BASE_DN
LDAP_PRIVILEGED_DN = settings.LDAP_PRIVILEGED_DN
SECRET_KEY = settings.SECRET_KEY
ALGORITHM  = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

class TokenData(BaseModel):
    username: str | None = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _get_ldap_connection(authentication=ANONYMOUS, user=None, password=None) -> Connection:
    """Create and return a new LDAP connection"""
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=user, password=password, authentication=authentication)
    conn.open()
    conn.bind()
    return conn

def _find_user_dn(username: str, search_base: str) -> Optional[str]:
    """
    Search for a user in the specified base DN
    Returns distinguished name (DN) if found, None otherwise
    """
    try:
        with _get_ldap_connection() as conn:
            conn.search(
                search_base=search_base,
                search_filter=f"(uid={username})",
                search_scope=SUBTREE
            )
            return conn.entries[0].entry_dn if conn.entries else None
    except Exception as e:
        logger.error(f"LDAP search failed in {search_base}: {str(e)}")
        return None

def _verify_credentials(user_dn: str, password: str) -> bool:
    """Verify user credentials by attempting to bind"""
    try:
        with _get_ldap_connection(user=user_dn, password=password, authentication=SIMPLE) as conn:
            return conn.bound
    except Exception as e:
        logger.error(f"LDAP bind failed for {user_dn}: {str(e)}")
        return False

def ldap_authenticate(username: str, password: str) -> Tuple[bool, bool]:
    """
    Authenticate user against LDAP with privilege check
    Returns:
        tuple: (is_authenticated, is_privileged)
    """
    if not username or not password:
        return False, False

    # First check privileged DN
    privileged_dn = _find_user_dn(username, LDAP_PRIVILEGED_DN)
    if privileged_dn and _verify_credentials(privileged_dn, password):
        logger.info(f"Privileged user {username} authenticated")
        return True, True

    # Fall back to base DN
    base_dn = _find_user_dn(username, LDAP_BASE_DN)
    if base_dn and _verify_credentials(base_dn, password):
        logger.info(f"Regular user {username} authenticated")
        return True, False

    logger.warning(f"Authentication failed for {username}")
    return False, False

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

async def get_token_from_cookie_or_header(
    token: str = Depends(oauth2_scheme),
    cookie_token: str = Cookie(default=None, alias="access_token")
):
    if cookie_token:
        return cookie_token
    if token:
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )


async def get_current_user(
        token: Annotated[str, Depends(get_token_from_cookie_or_header)],
        user_repository: UserRepositoryDep,
        ) -> UserPublic:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id = payload.get("sub")
        if id is None:
            raise credentials_exception

        user = user_repository.find_by_id(id)
        if user is None:
            raise credentials_exception
        
        if user:
            return UserPublic.from_orm(user)
        
    except  jwt.exceptions.InvalidTokenError:
        raise credentials_exception


def require_privileged_user(user: Annotated[UserPublic, Depends(get_current_user)]) -> UserPublic:
    if not user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges"
        )
    return user