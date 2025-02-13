import uuid
import os.path
from datetime import datetime as dt
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask import current_app as app
from flask_login import current_user, login_required
from .forms import CreateExerciseForm
from .utils import generate_unique_filename
from ..vm.services import clone_vm, create_new_template_vm, destroy_vm
from ..models import Exercise, User, TemplateVm, WorkVm, db




exercise_bp = Blueprint(
    'exercise_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@exercise_bp.route('/exercise/<int:id>', methods = ['GET'])
@login_required
def exercise(id):
    user_id = current_user.get_id() #get id of current user

    current_templatevm_id = Exercise.query.get(id).templatevm_id #get id of the templatevm of the exercise

    #get the id of the workvm of the current user and the current exercise
    current_user_workvm_id = WorkVm.query.filter_by(user_id = user_id, templatevm_id = current_templatevm_id).first().proxmox_id

    return render_template(
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
def exercises():
    exercises = {exercise.id: exercise.name for exercise in Exercise.query.all()}

    return render_template(
        'exercises.html',
        title="Exercises",
        description="Here you can see the list of available exercises.",
        template='exercises-template',
        exercises= exercises)


@exercise_bp.route('/exercise/create', methods = ['GET', 'POST'])
@login_required
def exercise_create():

    form = CreateExerciseForm()
    if form.validate_on_submit():#Verifies if method is POST
        filename = generate_unique_filename(form.gns3_file.data.filename)

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

                template_id = create_new_template_vm(form.proxmox_id.data, template_hostname , path_to_gns3project, commands_by_hostname)

                new_templatevm = TemplateVm(proxmox_id = template_id,
                                            created_on = dt.now()
                                            )

                db.session.add(new_templatevm)
                
                new_exercise = Exercise(name = form.title.data,
                                        description = form.body.data,
                                        templatevm = new_templatevm,
                                        created_on = dt.now()
                                        )
                
                db.session.add(new_exercise)

                existing_users = User.query.all()

                for user in existing_users:#TODO: this and the similar loop in auth should be refactored into a function, probably in vm.services
                    hostname = f'vm-{uuid.uuid4().hex[:12]}' #generate a random hostname


                    clone_id = clone_vm(new_exercise.templatevm.proxmox_id, hostname)

                    workvm = WorkVm(proxmox_id = clone_id,
                        user = user,
                        templatevm = new_exercise.templatevm,
                        created_on = dt.now(),
                        )
            
                    db.session.add(workvm)
            
                db.session.commit()
                
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}')
            return redirect(url_for('exercise_bp.exercise_create'))
        return redirect(url_for('exercise_bp.exercises'))

    return render_template(
        'create.html',
        title="Exercise creation",
        form=form,
        description="Here you can create a new exercise.",
        template='create-template'
        )

@exercise_bp.route('/exercise/<int:exercise_id>/delete', methods = ['POST']) #At this point in time this is only here deleting vms created for test purposes, not intended for real use
@login_required
def exercise_delete(exercise_id:int):
    try:
        exercise = Exercise.query.get(exercise_id)

        templatevm = exercise.templatevm

        workvms = templatevm.workvms

        with db.session.begin_nested():
            for workvm in workvms:
                destroy_vm(workvm.proxmox_id)
                db.session.delete(workvm)
            destroy_vm(templatevm.proxmox_id)
            db.session.delete(templatevm)
            db.session.delete(exercise)
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}')
        return redirect(request.referrer)#redirect back to the previous page
    return redirect(url_for('exercise_bp.exercises'))