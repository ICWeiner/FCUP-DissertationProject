from datetime import timedelta

from pydantic import BaseModel
from typing import Annotated
from fastapi import APIRouter, Request, Form, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.models import UserCreate, UserPublic, User
from app.dependencies.repositories import UserRepositoryDep, ExerciseRepositoryDep, WorkVmRepositoryDep
from app.dependencies.auth import CurrentUserDep, AuthorizedUserDep
from app.services import auth as auth_services
from app.services import vm as vm_services

from pathlib import Path

##TEMP
import jwt
SECRET_KEY = settings.SECRET_KEY
ALGORITHM  = settings.ALGORITHM

BASE_DIR = Path(__file__).parent.parent

router = APIRouter(tags=["users"],
                    responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory=str(BASE_DIR / "templates/"))

ACCESS_TOKEN_EXPIRE_SECONDS = settings.ACCESS_TOKEN_EXPIRE_SECONDS

class RegisterFormData(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


@router.get("/register", response_class=HTMLResponse)
async def create_user_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request,
                                                     "title": "Create an Account",
                                                     "body": "Sign up for a user account"})

@router.post("/register")
async def create_user(
    data: Annotated[RegisterFormData, Form()], 
    user_repository: UserRepositoryDep,
    exercise_repository: ExerciseRepositoryDep,
    workvm_repository: WorkVmRepositoryDep,
):
    user = UserCreate(username = data.username,
                      email = data.email,
                      hashed_password = auth_services.get_password_hash(data.password),
                      admin = False)
    
    db_user = User.model_validate(user)

    user_repository.save(db_user)

    workvms = await vm_services.create_users_work_vms( [db_user], exercise_repository.find_all() )

    workvm_repository.batch_save(workvms)

    return db_user

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
) -> Token:
    def _generate_token(response: Response, user: User) -> Token:
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
    
    user = user_repository.find_by_username(form_data.username)
    
    if user:
        # Verify local password
        if auth_services.verify_password(form_data.password, user.hashed_password):
            # Local authentication succeeded
            access_token = _generate_token(response, user)
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
    access_token = _generate_token(response, user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "is_privileged": is_privileged  # Optional: Include privilege status
    }

@router.get("/users/me")#test route to check if user is logged in
async def read_users_me(
    current_user: CurrentUserDep,
    user_repository: UserRepositoryDep,
): 
    user_public = user_repository.get_public(current_user)# if you want to return user info, use a UserPublic instance
    return user_public

@router.get("/users/me/authorized")#test route to check if user has privileges
async def read_users_me(
    current_user: AuthorizedUserDep,
): 
    return current_user
