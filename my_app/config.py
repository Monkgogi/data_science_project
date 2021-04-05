"""Flask config class."""
from pathlib import Path


class Config(object):
    """ Sets the Flask base configuration that is common to all environments. """
    DEBUG = False
    SECRET_KEY = '0qoEBdyfrssW-GwhhSVJtQ'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_PATH = Path(__file__).parent.parent.joinpath("data")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(DATA_PATH.joinpath('example.db'))
    # UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath("static").joinpath("img")
    UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath("static/img")


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_ECHO = True
    WTF_CSRF_ENABLED = False
