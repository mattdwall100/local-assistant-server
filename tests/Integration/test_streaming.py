from fastapi.testclient import TestClient

from assistant_server.main import create_app
from tests.mocks import create_mock_services


def test_synthesize_endpoint_streams_multiple_byte_chunks() -> None:
    # Arrange
    client = TestClient(create_app(service_factory=create_mock_services))

    # Act
    with client.stream(
        "POST",
        "/synthesize",
        json={"text": "hello", "session_id": "session-1"},
    ) as response:
        chunks = list(response.iter_bytes(chunk_size=4000))

    # Assert
    assert response.status_code == 200
    assert len(chunks) > 1
    assert all(isinstance(chunk, bytes) for chunk in chunks)
    assert all(chunk for chunk in chunks)
