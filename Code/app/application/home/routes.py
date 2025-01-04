from flask import Blueprint, render_template
from flask import current_app as app


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/', methods=["GET"])
@home_bp.route('/home', methods=["GET"])
def home():
    """Homepage."""

    return render_template(
        'home.html',
        title="GNS3 - Evaluation platform",
        description="GNS3 - Evaluation platform",
        template='home-template',)
