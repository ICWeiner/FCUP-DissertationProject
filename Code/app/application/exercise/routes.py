import uuid
import asyncio
import os.path
from datetime import datetime as dt
from quart import Blueprint, redirect, render_template, flash, request, session, url_for, jsonify
from quart import current_app as app
from quart_login import current_user, login_required
from .forms import CreateExerciseForm
from . import utils
from .. import gns3_tasks
from .. import proxmox_tasks
from ..models import Exercise, User, TemplateVm, WorkVm
from .. import db

import time
import logging

import psutil

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)


exercise_bp = Blueprint(
    'exercise_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@exercise_bp.route('/exercise/<int:id>', methods = ['GET'])
@login_required
async def exercise(id):
    user_id = current_user.get_id() #get id of current user

    current_templatevm_id = Exercise.query.get(id).templatevm_id #get id of the templatevm of the exercise

    #get the id of the workvm of the current user and the current exercise
    current_user_workvm_id = WorkVm.query.filter_by(user_id = user_id, templatevm_id = current_templatevm_id).first().proxmox_id

    return await render_template(
        'exercise.html',
        title="Exercise",
        description="Here you can see the details of a selected available exercises.",
        template='exercise-template',
        exercise_id=id,
        current_user_id = user_id,
        vm_proxmox_id = current_user_workvm_id,
        exercise_title="Sample Exercise")

@exercise_bp.route('/exercises', methods = ['GET'])
@login_required
async def exercises():
    exercises = {exercise.id: exercise.name for exercise in Exercise.query.all()}

    return await render_template(
        'exercises.html',
        title="Exercises",
        description="Here you can see the list of available exercises.",
        template='exercises-template',
        exercises= exercises)

@exercise_bp.route('/exercise/retrieve-hostnames', methods = ['POST'])
def retrieve_hostnames():
    if 'file' not in request.files:
        logging.warning('No file sent in the request for retrieve-hostnames')
        return jsonify({'error': 'No file part'}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    

    if not uploaded_file.filename.lower().endswith('.gns3project'):
        logging.warning('No file sent in the request for retrieve-hostnames')
        return jsonify({'error': 'Invalid file type. Only .gns3project files are allowed'}), 400

    try:
        nodes = utils.extract_node_names(uploaded_file)
        return jsonify(hostnamesList = nodes, success = True), 200
    except Exception as e:
        return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 400


@exercise_bp.route('/exercise/create', methods = ['GET', 'POST'])
@login_required
async def exercise_create():

    form = CreateExerciseForm()
    if form.validate_on_submit():#Verifies if method is POST
        filename = utils.generate_unique_filename(form.gns3_file.data.filename)

        path_to_gns3project = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        form.gns3_file.data.save(path_to_gns3project) #saves the gns3project file locally

        try:
            with db.session.begin_nested():
                template_hostname = f'tvm-{uuid.uuid4().hex[:18]}'#the length of this hostname can be extended up to 63 characters if more uniqueness is required

                commands_by_hostname = []

                #formats data in this manner [{'hostname': 'r1', 'commands': ['show version', 'ping 8.8.8.8']}, {'hostname': 'pc1', 'commands': ['traceroute 8.8.4.4']}] 
                for hostname_form in form.hostnames:
                    hostname_data = {
                        "hostname": hostname_form.hostname.data,
                        "commands": [command_form.data for command_form in hostname_form.commands]
                    }
                    commands_by_hostname.append(hostname_data)

                start_time_template_vm = time.perf_counter()
                
                #Step 1: Clone base template VM needs base template ID and hostname returns cloned vm ID
                vm_proxmox_id = await proxmox_tasks.aclone_vm(form.proxmox_id.data, template_hostname)

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

                new_templatevm = TemplateVm(proxmox_id = vm_proxmox_id,
                                            created_on = dt.now()
                                            )

                
                new_exercise = Exercise(name = form.title.data,
                                        description = form.body.data,
                                        templatevm = new_templatevm,
                                        created_on = dt.now()
                                        )
                

                existing_users = User.query.all()

                db.session.add(new_templatevm)
                db.session.add(new_exercise)

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
                            created_on = dt.now(),
                            )
                    db.session.add(workvm)

                logging.info("Done waiting for tasks to complete")
                
                end_time_clone_vms = time.perf_counter()

                logging.info(f"Template VM creation time: {end_time_template_vm - start_time_template_vm:.6f} seconds")
                logging.info(f"VM Cloning process time: {end_time_clone_vms - start_time_clone_vms:.6f} seconds")
                logging.info(f"Final CPU usage: {psutil.cpu_percent()}%")

                db.session.commit()
                
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}')
            return redirect(url_for('exercise_bp.exercise_create'))
        return redirect(url_for('exercise_bp.exercises'))

    return await render_template(
        'create.html',
        title="Exercise creation",
        form=form,
        description="Here you can create a new exercise.",
        template='create-template'
        )

@exercise_bp.route('/exercise/<int:exercise_id>/delete', methods = ['POST']) #At this point in time this is only here deleting vms created for test purposes, not intended for real use
@login_required
async def exercise_delete(exercise_id:int):#TODO: make async
    try:
        exercise = Exercise.query.get(exercise_id)

        templatevm = exercise.templatevm

        workvms = templatevm.workvms

        tasks = []

        with db.session.begin_nested():
            start_time_delete_vms = time.perf_counter()

            tasks = [proxmox_tasks.adestroy_vm(workvm.proxmox_id) for workvm in workvms]

            results = await asyncio.gather(*tasks)

            for workvm, result in zip(workvms, results):
                if isinstance(result, Exception):
                    logging.error(f"Error processing task result for {workvm}: {result}")
                elif result:
                    db.session.delete(workvm)
                else:
                    logging.error(f"Error deleting VM {workvm.proxmox_id}")
                    
            result = await proxmox_tasks.adestroy_vm(templatevm.proxmox_id)

            if isinstance(result, Exception):#TODO: DRY
                logging.error(f"Error processing task result for {workvm}: {result}")
            elif result:
                db.session.delete(templatevm)
                db.session.delete(exercise)
            else:
                logging.error(f"Error deleting VM {workvm.proxmox_id}")
            end_time_delete_vms = time.perf_counter() 

            logging.info(f"VM deleting process time: {end_time_delete_vms - start_time_delete_vms:.6f} seconds")
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}')
        return redirect(request.referrer)#redirect back to the previous page
    return redirect(url_for('exercise_bp.exercises'))