from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
import requests
from .forms import LoginForm, SignupForm
from ..models import db, User
from .. import login_manager
from datetime import datetime as dt
from werkzeug.exceptions import HTTPException



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
            user = User(
                username=form.username.data,
                email=form.email.data,
                created_on = dt.now()
            )
            user.set_password(form.password.data)
            db.session.add(user)
            #db.session.commit()  # Create new user


            # Send POST request to create the VM
            #TODO:This logic should be placed elsewhere, it creates a vm for a user
            '''
            vm_creation_url =  f'{}{url_for('vm_bp.create_vm', template_vm_id = 110)}'#TODO: remove this hard coding, retrieve from DB?
            data = {
                "email": form.email.data,
            }

            # Send the request and validate response
            try:
                response = requests.post(vm_creation_url, json=data)
                response.raise_for_status()  
            except HTTPException as e:
                flash(f"Failed to create VM: {e}")    
            '''
            login_user(user)
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