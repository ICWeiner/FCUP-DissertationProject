from pydantic import BaseModel
from sqlmodel import select
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from ..models import Exercise
from ..dependencies import SessionDep

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
async def check_list_exercises(request: Request, session: SessionDep):
    db_exercises = session.exec(select(Exercise)).all()
    exercises = {exercise.id: exercise.name for exercise in db_exercises}

    return templates.TemplateResponse('exercises.html', {"request": request,
                                                        "title" : "Exercises",
                                                        "description" : "Here you can see the list of available exercises",
                                                        "exercises" : exercises})


@router.get("/{exercise_id}", response_class=HTMLResponse)
async def check_exercise(request: Request, exercise_id: int, session: SessionDep):
    statement = select(Exercise).where(Exercise.id == exercise_id)
    exercise = session.exec(statement).first()
    return templates.TemplateResponse("exercise.html", {"request": request,
                                                     "title": exercise.name,
                                                     "body": exercise.description,
                                                     })

@router.post("/create")
async def create_exercise(session: SessionDep, data: Annotated[CreateExerciseFormData, Form()], gns3_file: UploadFile = File(...)):
    pass