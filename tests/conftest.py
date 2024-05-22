# conftest.py

import pytest
from .test_data import TAXIS_DATA, TRAJECTORIES_DATA
from src.app.app import app_
from config.config import TestingConfig
from src.models.models import Taxi, Trajectory

@pytest.fixture(scope='session')
def app():
    # Configura la aplicación con la configuración de prueba
    _app = app_
    _app.config.from_object(TestingConfig)
    yield _app

@pytest.fixture(scope='session')
def client(app):
    # Crea un cliente de prueba para la aplicación
    with app.test_client() as client:
        yield client
