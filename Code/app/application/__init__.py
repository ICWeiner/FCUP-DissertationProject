from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery, Task
import os


# Globally accessible libraries

db = SQLAlchemy()
login_manager = LoginManager()

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    
    db.init_app(app)
    login_manager.init_app(app)

    celery_init_app(app)

    with app.app_context():
        # Include our Routes
        from .home import routes as home
        from .vm import routes as vm
        from .test import routes as test
        from .exercise  import routes as exercise
        from .auth  import routes as auth
        from .provision_db import provision_data #creates a small amount of pre configured data for DB

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(vm.vm_bp)
        app.register_blueprint(test.test_bp)
        app.register_blueprint(exercise.exercise_bp)
        app.register_blueprint(auth.auth_bp)

        #db.create_all()
        if not os.path.exists('instance/my_database.db'):  # Check if the database exists
            print("#######################")
            print('DATABASE does not exist')
            print('creating new database')
            print("#######################")
            db.create_all()
            provision_data()

        return app  
    
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.name, task_cls=FlaskTask)
    celery.config_from_object(app.config['CELERY_CONFIG'])
    celery.set_default()
    app.extensions["celery"] = celery
    return celery