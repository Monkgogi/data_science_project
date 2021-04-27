from flask import Flask
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
photos = UploadSet('photos', IMAGES)

def create_app(config_classname):
    """
    Initialise and configure the Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """

    app = Flask(__name__)
    app.config.from_object(config_classname)

    register_dash_apps(app)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    csrf.init_app(app)
    # csrf._exempt_views.add('dash.dash.dispatch')
    configure_uploads(app, photos)

    with app.app_context():
        from my_app.models import User, Profile
        db.create_all()


def register_blueprints(app):
    from my_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from my_app.community.routes import community_bp
    app.register_blueprint(community_bp)

    from my_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)


def register_dash_apps(app):
    with app.app_context():
        from dash_app.dash import DashApp1
        dash_app1 = DashApp1(app)
        dash_app1.setup()
        _protect_dash_views(dash_app1.app)


def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
