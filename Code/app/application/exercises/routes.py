from flask import Blueprint, render_template
from flask import current_app as app


#TODO: FIX ABOVE IMPORTS

exercises_bp = Blueprint(
    'exercises_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@exercises_bp.route('/exercise/<int:id>')
def exercise(id):

    return render_template(
        'exercise.html',
        title="Exercise",
        description="Here you can see the details of a selected available exercises.",
        template='exercise-template',
        exercise=id,
        exercise_title="Sample Exercise")

@exercises_bp.route('/exercises')
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