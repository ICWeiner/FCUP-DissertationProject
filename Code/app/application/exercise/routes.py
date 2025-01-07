from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask import current_app as app
from flask_login import current_user, login_required
from .forms import CreateExerciseForm


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

@exercise_bp.route('/exercise/create', methods = ['GET'])
#@login_required
def exercise_create_page():

    form = CreateExerciseForm()
    if form.validate_on_submit():
        flash('Invalid username/password combination')
        return redirect(url_for('exercise_np.exercise_create_page'))

    return render_template(
        'create.html',
        title="Exercise creation",
        form=form,
        description="Here you can create a new exercise.",
        template='create-template'
        )