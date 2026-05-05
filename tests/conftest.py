import pytest
from fastapi.testclient import TestClient

from assistant_server.main import create_app
from .mocks import create_mock_services


@pytest.fixture
def client():
    app = create_app(service_factory=create_mock_services)
    return TestClient(app)

