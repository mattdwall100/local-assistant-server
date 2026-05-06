from importlib import import_module

import pytest
from fastapi.testclient import TestClient

from assistant_server.main import create_app
from .mocks import create_mock_services


# So that when app() is called, it can access the mock services wherever it is.
@pytest.fixture
def mock_services():
    return create_mock_services()


@pytest.fixture
def app(mock_services):
    return create_app(service_factory=lambda: mock_services)


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client
