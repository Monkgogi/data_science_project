from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_classname):
    """
    Initialise the Flask application.
    :type config_classname: Specifies the configuration class.
    :rtpye: Returns a configured flask Object
    """
    app = Flask(__name__)
    app.config.from_object(config_classname)
    # Initialise the SQLAlchemy object for the Flask app instance
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        # Import Dash application
        from dash_app.dash import init_dashboard
        app = init_dashboard(app)

    from My_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from My_app.community.routes import community_bp
    app.register_blueprint(community_bp)

    return app
