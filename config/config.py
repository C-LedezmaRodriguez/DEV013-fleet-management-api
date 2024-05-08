# config.py

import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRES_URL")

class TestingConfig(Config):
    TESTING = True
#     SQLALCHEMY_DATABASE_URI 

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
