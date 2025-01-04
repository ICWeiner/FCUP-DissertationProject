from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# Globally accessible libraries

db = SQLAlchemy()
login_manager = LoginManager()

'''
r = FlaskRedis()
'''

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    
    db.init_app(app)
    login_manager.init_app(app)
    '''
    r.init_app(app)
    '''

    with app.app_context():
        # Include our Routes
        from .home import routes as home
        from .vm import routes as vm
        from .test import routes as test
        from .exercise  import routes as exercise
        from .auth  import routes as auth

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(vm.vm_bp)
        app.register_blueprint(test.test_bp)
        app.register_blueprint(exercise.exercise_bp)
        app.register_blueprint(auth.auth_bp)

        db.create_all()

        return app