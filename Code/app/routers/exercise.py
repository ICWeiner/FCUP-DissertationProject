import uuid
import time
import os
import shutil
import json

import asyncio

from pydantic import BaseModel, ValidationError, parse_obj_as
from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List, Optional

from app.models import Exercise, TemplateVm
from app.dependencies.auth import CurrentUserDep, PrivilegedUserDep
from app.dependencies.repositories import ExerciseRepositoryDep, UserRepositoryDep, WorkVmRepositoryDep, TemplateVmRepositoryDep
from app.services import vm as vm_services
from app.services import proxmox as proxmox_services
from app.services import gns3 as gns3_services
from app.services import nornir as nornir_services
from app.utils import gns3 as gns3_utils

import psutil

from pathlib import Path

from logger.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).parent.parent

router = APIRouter(prefix="/exercises",
                    tags=["exercises"],
                    responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory=str(BASE_DIR / "templates/"))

class ValidationModel(BaseModel):
    hostname: str
    command: str 
    target: str 

class ConfigurationModel(BaseModel):
    hostname: str 
    commands: List[str] 

class CreateExerciseFormData(BaseModel):
    title: str 
    body: str
    proxmox_id: int
    gns3_file: UploadFile = File(...)
    validations: str
    configurations: Optional[str] = None


@router.get('/', response_class=HTMLResponse)
async def check_list_exercises(
    request: Request,
    exercise_repository: ExerciseRepositoryDep,
    workvm_repository: WorkVmRepositoryDep,
    current_user: CurrentUserDep,
):
    if current_user.admin:
        # Admin users see all exercises
        exercises = exercise_repository.find_all()
    else:
        # Non-admin users only see exercises they have WorkVMs for
        user_workvms = workvm_repository.find_by_user_id(current_user.id)
        exercise_ids = {workvm.templatevm.exercise.id for workvm in user_workvms if workvm.templatevm.exercise}
        exercises = exercise_repository.find_by_ids(list(exercise_ids)) if exercise_ids else []

    return templates.TemplateResponse('exercises.html', {
        "request": request,
        "title": "Exercises",
        "description": "Here you can see the list of available exercises",
        "exercises": exercises,
    })

@router.get('/create', response_class=HTMLResponse)
async def create_exercise_form(request: Request,
                            current_user: PrivilegedUserDep,
):
    return templates.TemplateResponse('create_exercise.html', {"request": request })

@router.post("/retrieve-hostnames")
async def retrieve_hostnames(gns3_file: UploadFile = File(...)):
    if not gns3_file.filename:
        logger.warning("No file sent in the request for retrieve-hostnames")
        raise HTTPException(status_code=400, detail="No file part")

    if not gns3_file.filename.lower().endswith(".gns3project"):
        logger.warning("Invalid file type sent in retrieve-hostnames request")
        raise HTTPException(status_code=400, detail="Invalid file type. Only .gns3project files are allowed")

    try:
        nodes = gns3_utils.extract_node_names(gns3_file.file)
        return JSONResponse(content={"hostnamesList": nodes, "success": True}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")


@router.get("/{exercise_id}", response_class=HTMLResponse)
async def check_exercise(request: Request,
                        exercise_id: int,
                        exercise_repository: ExerciseRepositoryDep,
                        workvm_repository: WorkVmRepositoryDep,
                        current_user: CurrentUserDep,
):
    
    exercise = exercise_repository.find_by_id(exercise_id)
    
    vm_proxmox_id = None

    work_vms = workvm_repository.find_by_users_and_exercise(current_user.id, exercise.id)

    if work_vms:
        vm_proxmox_id = work_vms[0].proxmox_id

    return templates.TemplateResponse("exercise.html", {"request": request,
                                                     "title": exercise.name,
                                                     "body": exercise.description,
                                                     "exercise_id": exercise_id,
                                                     "vm_proxmox_id": vm_proxmox_id,
                                                     })

@router.get("/{exercise_id}/manage", response_class=HTMLResponse)
async def manage_exercise(
    request: Request,
    exercise_id: int,
    exercise_repository: ExerciseRepositoryDep,
    user_repository: UserRepositoryDep,
    current_user: PrivilegedUserDep,
):
    # Get the exercise
    exercise = exercise_repository.find_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Get all users
    all_users = user_repository.find_all()
    
    # Get users already enlisted (have a workvm for this exercise)
    enlisted_users = user_repository.get_users_for_exercise(exercise_id)
    enlisted_user_ids = {u.id for u in enlisted_users}
    
    # Separate available and enlisted users
    available_users = [u for u in all_users if u.id not in enlisted_user_ids]
    
    return templates.TemplateResponse(
        "manage_exercise.html",
        {
            "request": request,
            "title": f"Manage {exercise.name}",
            "body": exercise.description,
            "exercise": exercise,
            "available_users": available_users,
            "enlisted_users": enlisted_users
        }
    )

@router.post("/{exercise_id}/manage/update", response_class=HTMLResponse)
async def update_exercise_enlistment(
    request: Request,
    exercise_id: int,
    exercise_repository: ExerciseRepositoryDep,
    user_repository: UserRepositoryDep,
    workvm_repository: WorkVmRepositoryDep,
    current_user: PrivilegedUserDep,
):
    form_data = await request.form()
    action = form_data.get("action")
    user_ids = form_data.getlist("user_ids")  # Get all selected user IDs
    
    if not action or not user_ids:
        raise HTTPException(status_code=400, detail="No action or users selected")
    
    # Get exercise to access templatevm_id
    exercise = exercise_repository.find_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    if action == "enlist":
        # Get users that don't already have workvms
        existing_user_ids = user_repository.get_users_for_exercise(exercise_id)
        
        new_user_ids = [uid for uid in user_ids if uid not in existing_user_ids]
        
        if new_user_ids:
            # Get full user objects
            users = user_repository.find_by_ids(new_user_ids)
            
            # Batch create VMs
            start_time = time.perf_counter()
            logger.info(f"Initial CPU usage: {psutil.cpu_percent()}%")
            logger.info(f"Cloning VMs for {len(users)} users")
            
            workvms = await vm_services.create_users_work_vms(users, [exercise])
            workvm_repository.batch_save(workvms)
            
            end_time = time.perf_counter()
            logger.info(f"VM Cloning process time: {end_time - start_time:.6f} seconds")
            logger.info(f"Final CPU usage: {psutil.cpu_percent()}%")
                
    elif action == "unlist":
        workvms = workvm_repository.find_by_users_and_exercise(
            user_ids=user_ids,
            exercise_id=exercise_id
        )
        
        if not workvms:
            return {"message": "No valid workvms found for deletion"}

        # Delete VMs in parallel
        start_time = time.perf_counter()
        logger.info(f"Starting deletion of {len(workvms)} VMs")

        tasks = [proxmox_services.adestroy_vm(workvm.proxmox_id) for workvm in workvms]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Log errors but continue with deletion
        for workvm, result in zip(workvms, results):
            if isinstance(result, Exception):
                logger.error(f"Error deleting VM {workvm.proxmox_id}: {result}")

        # Remove DB records
        workvm_repository.batch_delete(workvms)

        end_time = time.perf_counter()
        logger.info(f"VM deletion process time: {end_time - start_time:.6f} seconds")
    
    # Redirect back to management page
    return RedirectResponse(
        url=f"/exercises/{exercise_id}/manage",
        status_code= 302
    )

@router.post("/{exercise_id}/validate")
async def evaluate_exercise(exercise_repository: ExerciseRepositoryDep,
                        workvm_repository: WorkVmRepositoryDep,
                        current_user: CurrentUserDep,
                        exercise_id: int,
):  
    exercise = exercise_repository.find_by_id(exercise_id)

    gns3_project_id = exercise.templatevm.gns3_project_id

    vm_proxmox_id = None

    work_vms = workvm_repository.find_by_users_and_exercise(current_user.id, exercise.id)

    if work_vms:
        vm_proxmox_id = work_vms[0].proxmox_id

    validations = json.loads(exercise.validations)

    results = []

    await proxmox_services.aset_vm_status(vm_proxmox_id, True)

    node_ip = await proxmox_services.aget_vm_ip(vm_proxmox_id)

    await asyncio.sleep(3)

    gns3_config_filename = await gns3_services.setup_gns3_project(node_ip, gns3_project_id, "test")#test hostname needs to be replaced by vm hostname

    for validation in validations:    
        result = nornir_services.run_command(validation['hostname'], validation['command'], validation['target'], gns3_config_filename)
        results.append(result)

    return {
        "validations": exercise.validations,
        "configurations": exercise.configurations,
        "results": results,
    }
    

@router.post("/create")
async def create_exercise(exercise_repository: ExerciseRepositoryDep,
                        templatevm_repository: TemplateVmRepositoryDep,
                        current_user: PrivilegedUserDep,
                        data: Annotated[CreateExerciseFormData, Form()],
):  
    
    validations = json.loads(data.validations)
    configurations = (
        json.loads(data.configurations)
        if data.configurations else None
    )

    filename = gns3_utils.generate_unique_filename(data.gns3_file.filename)

    path_to_gns3project = os.path.join(str(BASE_DIR / "uploads"), filename)

    with open(path_to_gns3project, "wb") as buffer:
        shutil.copyfileobj(data.gns3_file.file, buffer)

    template_hostname = f'tvm-{uuid.uuid4().hex[:18]}'#the length of this hostname can be extended up to 63 characters if more uniqueness is required

    start_time_template_vm = time.perf_counter()
    
    #Step 1: Clone base template VM needs base template ID and hostname returns cloned vm ID
    vm_proxmox_id = await proxmox_services.aclone_vm(data.proxmox_id, template_hostname)

    # Step 2: Start VM needs vm ID returns true if successful
    await proxmox_services.aset_vm_status(vm_proxmox_id, True)

    node_ip = await proxmox_services.aget_vm_ip(vm_proxmox_id)

    await asyncio.sleep(3)

    # Step 3: Import GNS3 Project needs vm IP returns GNS3 project ID
    gns3_project_id = await gns3_services.import_gns3_project(node_ip, path_to_gns3project) 

    # Step 4: Run Commands on GNS3 (this is highly specific to this workflow) needs vm IP
    if configurations:
        gns3_config_filename= await gns3_services.setup_gns3_project(node_ip, gns3_project_id, template_hostname)
        for configuration in configurations:
            for command in configuration['commands']:
                #here its intended to use our developed Generic Module for nornir hence the "" as this parameter isnt used by this module 
                nornir_services.run_command(configuration['hostname'], command, "", gns3_config_filename)

    # Step 5: Stop VM needs VM ID returns true if successful
    await proxmox_services.aset_vm_status(vm_proxmox_id, False)

    # Step 6: Convert to Template needs VM id returns true if successful
    await proxmox_services.atemplate_vm(vm_proxmox_id) 

    end_time_template_vm = time.perf_counter() 

    new_templatevm = TemplateVm(proxmox_id = vm_proxmox_id,
                                gns3_project_id = str(gns3_project_id),
                                hostname = template_hostname)

    new_exercise = Exercise(name = data.title,
                            description = data.body,
                            templatevm = new_templatevm,
                            validations = json.dumps(validations),
                            configurations = json.dumps(configurations)
                            )
    
    logger.info(f"Template VM creation time: {end_time_template_vm - start_time_template_vm:.6f} seconds")

    exercise_repository.save(new_exercise)
    templatevm_repository.save(new_templatevm)#TODO: validate with pydantic

    return {"message": "Exercise created sucessfully"}

@router.post("/exercise/{exercise_id}/delete")
async def exercise_delete(exercise_id: int,
                        exercise_repository: ExerciseRepositoryDep,
                        current_user: PrivilegedUserDep,
):
    try:
        exercise = exercise_repository.find_by_id(exercise_id)

        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")

        templatevm = exercise.templatevm

        workvms = templatevm.workvms

        start_time = time.perf_counter()

        tasks = [proxmox_services.adestroy_vm(workvm.proxmox_id) for workvm in workvms]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for workvm, result in zip(workvms, results):
            if isinstance(result, Exception):
                logger.error(f"Error deleting VM {workvm.proxmox_id}: {result}")

        # Delete the template VM
        template_result = await proxmox_services.adestroy_vm(templatevm.proxmox_id)

        if isinstance(template_result, Exception):
            logger.error(f"Error deleting template VM {templatevm.proxmox_id}: {template_result}")

        end_time = time.perf_counter()
        logger.info(f"VM deletion process time: {end_time - start_time:.6f} seconds")

        exercise_repository.delete_by_id(exercise.id) #SQLmodel will delete the associated templateVM and workVMs

        return {"message": "Exercise deleted successfully"}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the exercise")