from datetime import timedelta

from pydantic import BaseModel
from typing import Annotated
from fastapi import APIRouter, Request, Form, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.models import UserCreate, User
from app.dependencies.repositories import UserRepositoryDep
from app.dependencies.auth import CurrentUserDep, PrivilegedUserDep, ProxmoxSessionManagerDep
from app.services import auth as auth_services

from pathlib import Path

ACCESS_TOKEN_EXPIRE_SECONDS = settings.ACCESS_TOKEN_EXPIRE_SECONDS

LDAP_BASE_REALM = settings.LDAP_BASE_REALM
LDAP_PRIVILEGED_REALM = settings.LDAP_PRIVILEGED_REALM


BASE_DIR = Path(__file__).parent.parent

router = APIRouter(tags=["users"],
                    responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory=str(BASE_DIR / "templates/"))

class RegisterFormData(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def _generate_and_set_token(response: Response, user: User) -> Token:
    """Helper to generate token and set cookie"""
    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token = auth_services.create_access_token(
        data={
            "sub": str(user.id),
            "is_privileged": user.admin
        },
        expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_SECONDS,
        secure=False,  # True in production
        samesite="lax",
        path="/"
    )
    return access_token


@router.get("/register", response_class=HTMLResponse)
async def create_user_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request,
                                                     "title": "Create an Account",
                                                     "body": "Sign up for a user account"})

@router.post("/register")
async def create_user(
    response: Response,
    data: Annotated[RegisterFormData, Form()], 
    user_repository: UserRepositoryDep,
):
    user = UserCreate(username = data.username,
                      email = data.email,
                      hashed_password = auth_services.get_password_hash(data.password),
                      admin = False,
                      realm = "pam")
    
    db_user = User.model_validate(user)

    user_repository.save(db_user)

    _generate_and_set_token(response, db_user)

    return db_user.model_dump()

@router.get("/login", response_class=HTMLResponse)
async def login_user_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,
                                                     "title": "Log in",
                                                     "body": "Log in with your User account"})

@router.post("/login")
async def login_user(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: UserRepositoryDep,
    proxmox_session_manager :ProxmoxSessionManagerDep,
) -> Token:
    user = user_repository.find_by_username(form_data.username)

    if user:
        # Existing user - try auth with their stored realm
        success, is_privileged = await proxmox_session_manager.verify_credentials(
            username=form_data.username,
            password=form_data.password,
            realm=user.realm  # Use the realm from database
        )
    else:
        # New user - try LDAP realms
        success, is_privileged = await proxmox_session_manager.verify_credentials(
            username=form_data.username,
            password=form_data.password
            # Let verify_credentials handle the realm fallback
        )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    # Create user if they don't exist
    if not user:
        user = User(
            username=form_data.username,
            email=f"{form_data.username}@fakedomain.com",
            hashed_password=auth_services.get_password_hash(form_data.password),
            admin=is_privileged,
            realm=settings.LDAP_PRIVILEGED_REALM if is_privileged else settings.LDAP_BASE_REALM
        )
        user_repository.save(user)

    access_token = _generate_and_set_token(response, user)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

    
    """
    user = user_repository.find_by_username(form_data.username)
    
    if user:
        # Verify local password
        if auth_services.verify_password(form_data.password, user.hashed_password):
            # Local authentication succeeded
            access_token = _generate_and_set_token(response, user)
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }

    # Step 2: Local auth failed, try LDAP
    ldap_success, is_privileged = auth_services.ldap_authenticate(
        form_data.username,
        form_data.password
    )
    
    if not ldap_success:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    # Step 3: LDAP succeeded - register local user
    if not user:
        # Create new user
        user = User(
            username=form_data.username,
            email=f"{form_data.username}@fakedomain.com",  # Adjust as needed
            hashed_password=auth_services.get_password_hash(form_data.password),
            admin=is_privileged,
        )
        user_repository.save(user)

    # Step 4: Generate token for newly registered/updated user
    access_token = _generate_and_set_token(response, user)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    """

@router.get("/me")#test route to check if user is logged in
async def read_users_me(
    current_user: CurrentUserDep,
    user_repository: UserRepositoryDep,
): 
    user_public = user_repository.get_public(current_user)# if you want to return user info, use a UserPublic instance
    return user_public.model_dump()

@router.get("/auth")#test route to check if user has privileges
async def read_users_me_auth(
    current_user: PrivilegedUserDep,
): 
    return current_user.model_dump()
