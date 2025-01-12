from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask import current_app as app
from flask_login import current_user, login_required
from datetime import datetime as dt
from .forms import CreateExerciseForm
from ..vm.routes import create_vm_for_new_exercise
from ..models import Exercise, User, TemplateVm, WorkVm, db



exercise_bp = Blueprint(
    'exercise_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@exercise_bp.route('/exercise/<int:id>', methods = ['GET'])
#@login_required
def exercise(id):

    return render_template(
        'exercise.html',
        title="Exercise",
        description="Here you can see the details of a selected available exercises.",
        template='exercise-template',
        exercise=id,
        exercise_title="Sample Exercise")

@exercise_bp.route('/exercises', methods = ['GET'])
#@login_required
def exercises():

    return render_template(
        'exercises.html',
        title="Exercises",
        description="Here you can see the list of available exercises.",
        template='exercises-template',
        exercises={
            1: 'Sample Exercise Number 1 ',
            2: 'Sample Exercise Number 2'
        })

@exercise_bp.route('/exercise/create', methods = ['GET', 'POST'])
#@login_required
def exercise_create():

    form = CreateExerciseForm()
    if form.validate_on_submit():#Verifies if method is POST
        try:
            with db.session.begin_nested():

                new_templatevm = TemplateVm(templatevm_proxmox_id=110,
                                            created_on = dt.now())

                db.session.add(new_templatevm)

                new_exercise = Exercise(name = 'exercise',
                                        description = 'Lorem ipsum',
                                        templatevm = new_templatevm,
                                        created_on = dt.now()
                                        )
                
                db.session.add(new_exercise)

                user = User(username = 'user',#TODO:only here for tests purposes REMOVE
                            email = 'test@mail.com',
                            password = 'testpass',
                            created_on = dt.now(),
                            )
                
                db.session.add(user)

                existing_users = User.query.all()

                for user in existing_users: 
                    hostname = f'{user.username}{new_exercise.name}'

                    print('#############################')
                    print(new_exercise.templatevm.templatevm_proxmox_id)
                    print('#############################')

                    print('#############################')
                    print(new_exercise.templatevm_id)
                    print('#############################')
                    clone_id = create_vm_for_new_exercise(new_exercise.templatevm.templatevm_proxmox_id, hostname)

                    workvm = WorkVm(workvm_proxmox_id = clone_id,
                        user = user,
                        templatevm = new_exercise.templatevm,
                        created_on = dt.now(),
                        )
            
                    db.session.add(workvm)
            
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}')
        return redirect(url_for('exercise_bp.exercises'))

    return render_template(
        'create.html',
        title="Exercise creation",
        form=form,
        description="Here you can create a new exercise.",
        template='create-template'
        )