from flask import Flask
from flask_login import LoginManager
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

    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    csrf.init_app(app)
    configure_uploads(app, photos)

    with app.app_context():
        from my_app.models import User, Profile, Area
        db.create_all()

        # Import Dash application
        from dash_app.dash import init_dashboard
        init_dashboard(app)

        from my_app.models import User
        db.create_all()

    from my_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from my_app.community.routes import community_bp
    app.register_blueprint(community_bp)

    from my_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app





