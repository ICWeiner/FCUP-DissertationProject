import uuid
import time
import os
import shutil

import asyncio

from pydantic import BaseModel
from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List, Optional

from app.models import Exercise, WorkVm, TemplateVm
from app.dependencies.auth import CurrentUserDep
from app.dependencies.repositories import ExerciseRepositoryDep, UserRepositoryDep, WorkVmRepositoryDep, TemplateVmRepositoryDep
from app.services import proxmox as proxmox_tasks
from app.services import gns3 as gns3_tasks
from app.utils import gns3 as gns3_utils

import logging
import psutil

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)

router = APIRouter(prefix="/exercises",
                    tags=["exercises"],
                    responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory=str(BASE_DIR / "templates/"))

class HostnameModel(BaseModel):
    hostname: str 
    commands: List[str] 

class CreateExerciseFormData(BaseModel):
    title: str
    body: str
    proxmox_id: int
    gns3_file: UploadFile = File(...)
    hostnames: Optional[List[HostnameModel]] = None

@router.get('/', response_class=HTMLResponse)
async def check_list_exercises(request: Request,
                            exercise_repository: ExerciseRepositoryDep,
                            current_user: CurrentUserDep,
):
    exercises = exercise_repository.find_all()

    return templates.TemplateResponse('exercises.html', {"request": request,
                                                        "title" : "Exercises",
                                                        "description" : "Here you can see the list of available exercises",
                                                        "exercises" : exercises})

@router.get('/create', response_class=HTMLResponse)
async def create_exercise_form(request: Request,
                            #current_user: CurrentUserDep,
):
    return templates.TemplateResponse('create_exercise.html', {"request": request })

@router.post("/retrieve-hostnames")
async def retrieve_hostnames(gns3_file: UploadFile = File(...)):
    if not gns3_file.filename:
        logging.warning("No file sent in the request for retrieve-hostnames")
        raise HTTPException(status_code=400, detail="No file part")

    if not gns3_file.filename.lower().endswith(".gns3project"):
        logging.warning("Invalid file type sent in retrieve-hostnames request")
        raise HTTPException(status_code=400, detail="Invalid file type. Only .gns3project files are allowed")

    try:
        nodes = gns3_utils.extract_node_names(gns3_file.file)
        return JSONResponse(content={"hostnamesList": nodes, "success": True}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")


@router.get("/{exercise_id}", response_class=HTMLResponse)#TODO: implement finding user's id and related vm
async def check_exercise(request: Request,
                        exercise_repository: ExerciseRepositoryDep,
                        exercise_id: int,
                        #current_user: CurrentUserDep,

):
    exercise = exercise_repository.find_by_id(exercise_id)

    return templates.TemplateResponse("exercise.html", {"request": request,
                                                     "title": exercise.name,
                                                     "body": exercise.description,
                                                     "exercise_id": exercise_id,
                                                     })

@router.post("/create")
async def create_exercise(exercise_repository: ExerciseRepositoryDep,
                        user_repository: UserRepositoryDep,
                        templatevm_repository: TemplateVmRepositoryDep,
                        workvm_repository: WorkVmRepositoryDep,
                        #current_user: CurrentUserDep,
                        data: Annotated[CreateExerciseFormData, Form()],
):  
    filename = gns3_utils.generate_unique_filename(data.gns3_file.filename)

    path_to_gns3project = os.path.join(str(BASE_DIR / "uploads"), filename)

    with open(path_to_gns3project, "wb") as buffer:
        shutil.copyfileobj(data.gns3_file.file, buffer)

    template_hostname = f'tvm-{uuid.uuid4().hex[:18]}'#the length of this hostname can be extended up to 63 characters if more uniqueness is required

    commands_by_hostname = []
    
    #formats data in this manner [{'hostname': 'r1', 'commands': ['show version', 'ping 8.8.8.8']}, {'hostname': 'pc1', 'commands': ['traceroute 8.8.4.4']}] 
    if data.hostnames:
        for hostname_form in data.hostnames:
            hostname_data = {
                "hostname": hostname_form.hostnames,
                "commands": [command_form.data for command_form in hostname_form.commands]#TODO this isnt right
            }
            commands_by_hostname.append(hostname_data)
    
    start_time_template_vm = time.perf_counter()
    
    #Step 1: Clone base template VM needs base template ID and hostname returns cloned vm ID
    vm_proxmox_id = await proxmox_tasks.aclone_vm(data.proxmox_id, template_hostname)

    # Step 2: Start VM needs vm ID returns true if successful
    await proxmox_tasks.aset_vm_status(vm_proxmox_id ,True)

    node_ip = await proxmox_tasks.aget_vm_ip(vm_proxmox_id)

    # Step 3: Import GNS3 Project needs vm IP returns GNS3 project ID
    gns3_project_id = gns3_tasks.import_gns3_project(node_ip, path_to_gns3project) 

    # Step 4: Run Commands on GNS3 (this is highly specific to this workflow) needs vm IP
    if commands_by_hostname:
        gns3_tasks.run_gns3_commands(node_ip, gns3_project_id, template_hostname, commands_by_hostname) 

    # Step 5: Stop VM needs VM ID returns true if successful
    await proxmox_tasks.aset_vm_status(vm_proxmox_id, False)

    # Step 6: Convert to Template needs VM id returns true if successful
    await proxmox_tasks.atemplate_vm(vm_proxmox_id) 

    end_time_template_vm = time.perf_counter() 

    new_templatevm = TemplateVm(proxmox_id = vm_proxmox_id)
    
    new_exercise = Exercise(name = data.title,
                            description = data.body,
                            templatevm = new_templatevm,
                            )

    existing_users = user_repository.find_all()

    exercise_repository.save(new_exercise)
    templatevm_repository.save(new_templatevm)#TODO: validate with pydantic
    exercise_repository.save(new_exercise)

    start_time_clone_vms = time.perf_counter()
        
    logging.info(f"Initial CPU usage: {psutil.cpu_percent()}%")
    
    logging.info(f"Cloning VMs for {len(existing_users)} users")

    tasks = []

    for _ in range(len(existing_users)):
        hostname = f'vm-{uuid.uuid4().hex[:12]}' #generate a random hostname
        tasks.append(proxmox_tasks.aclone_vm(new_exercise.templatevm.proxmox_id, hostname))
    vm_ids = await asyncio.gather(*tasks)

    for user, vm_id in zip(existing_users, vm_ids):
        workvm = WorkVm(
                proxmox_id = vm_id,
                user = user,
                templatevm = new_exercise.templatevm,
                )
        workvm_repository.save(workvm)#TODO:validate with pydantic TODO: instead of saving one by one do by batch

    logging.info("Done waiting for tasks to complete")
    
    end_time_clone_vms = time.perf_counter()

    logging.info(f"Template VM creation time: {end_time_template_vm - start_time_template_vm:.6f} seconds")
    logging.info(f"VM Cloning process time: {end_time_clone_vms - start_time_clone_vms:.6f} seconds")
    logging.info(f"Final CPU usage: {psutil.cpu_percent()}%")


    return

@router.post("/exercise/{exercise_id}/delete")
async def exercise_delete(exercise_id: int,
                        exercise_repository: ExerciseRepositoryDep,
                        #current_user: CurrentUserDep,
):
    try:
        exercise = exercise_repository.find_by_id(exercise_id)

        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")

        templatevm = exercise.templatevm

        workvms = templatevm.workvms

        start_time = time.perf_counter()

        tasks = [proxmox_tasks.adestroy_vm(workvm.proxmox_id) for workvm in workvms]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for workvm, result in zip(workvms, results):
            if isinstance(result, Exception):
                logging.error(f"Error deleting VM {workvm.proxmox_id}: {result}")

        # Delete the template VM
        template_result = await proxmox_tasks.adestroy_vm(templatevm.proxmox_id)

        if isinstance(template_result, Exception):
            logging.error(f"Error deleting template VM {templatevm.proxmox_id}: {template_result}")

        end_time = time.perf_counter()
        logging.info(f"VM deletion process time: {end_time - start_time:.6f} seconds")

        exercise_repository.delete_by_id(exercise.id) #SQLmodel will delete the associated templateVM and workVMs

        return {"message": "Exercise deleted successfully"}

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the exercise")