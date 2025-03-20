from quart import Quart 
from quart_sqlalchemy import SQLAlchemy, SQLAlchemyConfig
from quart_auth import QuartAuth
import os


# Globally accessible libraries

db = SQLAlchemy(
    SQLAlchemyConfig(
        database_url="sqlite+aiosqlite:///my_database.db",  # Use an async driver like `aiosqlite`
        echo=True  # Optional: Set to True for debugging queries
    )
)
auth_manager = QuartAuth()

def init_app():
    """Initialize the core application."""
    app = Quart(__name__)
    app.config.from_object('config.Config')

    # Initialize Plugins
    
    #await auth_manager.init_app(app)

    auth_manager.init_app(app)

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
    