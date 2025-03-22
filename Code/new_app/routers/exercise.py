from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from typing import Annotated, List
from ..models import Exercise
from ..dependencies import get_session

router = APIRouter(prefix="/exercises",
                    tags=["exercises"],
                    responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory="templates")


class HostnameModel(BaseModel):
    hostname: str

class CreateExerciseFormData(BaseModel):
    title: str
    body: str
    proxmox_id: str
    hostnames: List[HostnameModel]


@router.get('/', response_class=HTMLResponse)
def check_list_exercises(request: Request, session = Depends(get_session)):
    db_exercises = session.exec(select(Exercise)).all()
    exercises = {exercise.id: exercise.name for exercise in db_exercises}

    return templates.TemplateResponse('exercises.html', {"request": request,
                                                        "title" : "Exercises",
                                                        "description" : "Here you can see the list of available exercises.",
                                                        "exercises" : exercises})



@router.get("/id", response_class=HTMLResponse)
async def check_exercise(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request,
                                                     "title": "Create an Account",
                                                     "body": "Sign up for a user account"})

@router.post("/create")
async def create_user(data: Annotated[CreateExerciseFormData, Form()], gns3_file: UploadFile = File(...), session = Depends(get_session)):
    pass