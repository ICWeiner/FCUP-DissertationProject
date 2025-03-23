from datetime import timedelta

import os
from dotenv import load_dotenv

from pydantic import BaseModel
from typing import Annotated
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

from ..models import UserCreate, UserPublic, User
from ..dependencies.auth import UserRepositoryDep
from ..services import auth as auth_services

router = APIRouter(tags=["users"],
                    responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory="templates")

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

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
):
    user = UserCreate(username = data.username,
                      email = data.email,
                      hashed_password = auth_services.get_password_hash(data.password),
                      admin = False)
    db_user = User.model_validate(user)
    user_repository.save(db_user)
    return db_user

@router.get("/login", response_class=HTMLResponse)
async def login_user_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,
                                                     "title": "Log in",
                                                     "body": "Log in with your User account"})

@router.post("/login")
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: UserRepositoryDep,
) -> Token:
    user = user_repository.find_by_username(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    success = auth_services.verify_password(form_data.password, user.hashed_password)

    if not success:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[UserPublic, Depends(auth_services.get_current_user)],
):
    return current_user