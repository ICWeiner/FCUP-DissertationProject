from pydantic import BaseModel
from sqlmodel import select
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from ..models import Exercise
from ..dependencies.repositories import ExerciseRepositoryDep

router = APIRouter(prefix="/exercises",
                    tags=["exercises"],
                    responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory="templates")


class HostnameModel(BaseModel):
    hostname: str
    commands: List[str]

class CreateExerciseFormData(BaseModel):
    title: str
    body: str
    proxmox_id: int
    #hostnames: List[HostnameModel]


@router.get('/', response_class=HTMLResponse)
async def check_list_exercises(request: Request,
                               exercise_repository: ExerciseRepositoryDep
):
    exercises = exercise_repository.find_all()

    return templates.TemplateResponse('exercises.html', {"request": request,
                                                        "title" : "Exercises",
                                                        "description" : "Here you can see the list of available exercises",
                                                        "exercises" : exercises})


@router.get("/{exercise_id}", response_class=HTMLResponse)
async def check_exercise(request: Request,
                        exercise_repository: ExerciseRepositoryDep,
                        exercise_id: int
):
    exercise = exercise_repository.find_by_id(exercise_id)

    return templates.TemplateResponse("exercise.html", {"request": request,
                                                     "title": exercise.name,
                                                     "body": exercise.description,
                                                     })

@router.post("/create")
async def create_exercise(exercise_repository: ExerciseRepositoryDep,
                        data: Annotated[CreateExerciseFormData, Form()],
                        #   gns3_file: UploadFile = File(...)
):
    exercise = Exercise (name = data.title,
                         description = data.body,
                         templatevm_id = data.proxmox_id)
    
    
    db_exercise = Exercise.model_validate(exercise)
    
    exercise_repository.save(db_exercise)

    return db_exercise
    
    #do stuff with "data.hostnames"

    #do stuff with gns3_file