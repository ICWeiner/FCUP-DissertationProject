from flask import Flask


# Globally accessible libraries
'''
db = SQLAlchemy()
r = FlaskRedis()
'''

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    ''' 
    db.init_app(app)
    r.init_app(app)
    '''

    with app.app_context():
        # Include our Routes
        from .home import routes as home
        from .vm import routes as vm

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(vm.vm_bp)

        return app