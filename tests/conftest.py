# conftest.py

import pytest
from src.app.app import app
from config.config import TestingConfig

@pytest.fixture(scope='module')
def create_app():
    _new_app = app
    _new_app.config.from_object(TestingConfig)
    yield _new_app

@pytest.fixture(scope='module')
def client():
    with app.test_client() as client:
        yield client
