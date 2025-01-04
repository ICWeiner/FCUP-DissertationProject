from flask import Blueprint, render_template
from flask import current_app as app
from flask_login import current_user, login_required


exercise_bp = Blueprint(
    'exercise_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@exercise_bp.route('/exercise/<int:id>')
#@login_required
def exercise(id):

    return render_template(
        'exercise.html',
        title="Exercise",
        description="Here you can see the details of a selected available exercises.",
        template='exercise-template',
        exercise=id,
        exercise_title="Sample Exercise")

@exercise_bp.route('/exercises')
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