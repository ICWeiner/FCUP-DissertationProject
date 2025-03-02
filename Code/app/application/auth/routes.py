import uuid
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import LoginForm, SignupForm
from ..models import Exercise, User, TemplateVm, WorkVm, db
from ..vm.services import celery_clone_vm_task
from .. import login_manager
from datetime import datetime as dt

import logging

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)

auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit(): #this function already checks if request is POST
        user = User.query.filter_by(email=form.email.data).first() #check if email is registered in db
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('exercise_bp.exercises'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template(
        'login.html',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit(): 
        existing_user = User.query.filter_by(email=form.email.data).first() 
        if existing_user is None:
            try:
                with db.session.begin_nested():
                    new_user = User(
                        username=form.username.data,
                        email=form.email.data,
                        created_on = dt.now()
                    )
                    new_user.set_password(form.password.data)

                    db.session.add(new_user)

                    existing_exercises = Exercise.query.all()

                    task_results = []

                    for exercise in existing_exercises:#TODO: this and the similar loop in auth should be refactored into a function, probably in vm.services
                        hostname = f'vm-{uuid.uuid4().hex[:12]}' #generate a random hostname

                        result = celery_clone_vm_task.apply_async(args=[exercise.templatevm.proxmox_id, hostname])

                        # Store the task result for later processing
                        task_results.append((exercise, result))

                    logging.info(f"Waiting for {len(task_results)} tasks to complete")
                    
                    for exercise, result in task_results:
                        try:
                            # Get the result from the task (blocking for completion)
                            clone_id = result.get(timeout=300)  # You can adjust the timeout as needed
                            
                            # Now create the WorkVm entry for this user
                            workvm = WorkVm(
                                proxmox_id = clone_id,
                                user = new_user,
                                templatevm = exercise.templatevm,
                                created_on = dt.now(),
                                )
                            db.session.add(workvm)

                        except Exception as e:
                            print(f"Error processing task result for {exercise}: {e}")
                    db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}')
                return redirect(url_for('auth_bp.signup'))

            login_user(new_user)
            return redirect(url_for('exercise_bp.exercises'))
        flash('A user already exists with that email address.')
    return render_template(
        'signup.html',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('home_bp.home'))