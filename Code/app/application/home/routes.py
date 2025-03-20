from quart import Blueprint, render_template
from quart import current_app as app


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/', methods=["GET"])
@home_bp.route('/home', methods=["GET"])
async def home():
    """Homepage."""

    return await render_template(
        'home.html',
        title="GNS3 - Evaluation platform",
        description="GNS3 - Evaluation platform",
        template='home-template',)
