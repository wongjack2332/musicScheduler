import pytest
from src.main import create_app


@pytest.fixture()
def app():
    return create_app()


@pytest.fixture()
def client(app):
    client = app.test_client()
    return client
