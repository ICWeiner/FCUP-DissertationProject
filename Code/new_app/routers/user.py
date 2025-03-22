from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from ..models import User, UserCreate
from ..dependencies import get_session

router = APIRouter(prefix="/users",
                    tags=["users"],
                    responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory="templates")

class RegisterFormData(BaseModel):
    username: str
    email: str
    password: str

class LoginFormData(BaseModel):
    email: str
    password: str


@router.get("/register", response_class=HTMLResponse)
async def create_user_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request,
                                                     "title": "Create an Account",
                                                     "body": "Sign up for a user account"})

@router.post("/register")
async def create_user(data: Annotated[RegisterFormData, Form()], session = Depends(get_session)):
    user = UserCreate(username = data.username,
                      email = data.email,
                      password = data.password)
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/login", response_class=HTMLResponse)
async def login_user_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,
                                                     "title": "Log in",
                                                     "body": "Log in with your User account"})

@router.post("/login")
async def login_user(data: Annotated[RegisterFormData, Form()], session = Depends(get_session)):
    pass #TODO: implement login