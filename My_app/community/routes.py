from flask import Blueprint, render_template

community_bp = Blueprint('community_bp', __name__, url_prefix='/community')


@community_bp.route('/')
def index():
    return render_template('index.html', title='Home page ')
