"""
Integration tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "title" in data["data"]


def test_list_tools(client):
    """Test list tools endpoint."""
    response = client.get("/api/tools")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "tools" in data["data"]
    assert len(data["data"]["tools"]) > 0

    # Check tool names
    tool_names = [tool["name"] for tool in data["data"]["tools"]]
    assert "get_weather" in tool_names
    assert "github_user_lookup" in tool_names
    assert "summarize_text" in tool_names
    assert "system_status" in tool_names


def test_list_resources(client):
    """Test list resources endpoint."""
    response = client.get("/api/resources")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "resources" in data["data"]


def test_get_resource(client):
    """Test get resource endpoint."""
    response = client.get("/api/resources/server_status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data


def test_get_nonexistent_resource(client):
    """Test get nonexistent resource."""
    response = client.get("/api/resources/nonexistent")
    assert response.status_code == 404


def test_list_prompts(client):
    """Test list prompts endpoint."""
    response = client.get("/api/prompts")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "prompts" in data["data"]


def test_get_prompt(client):
    """Test get prompt endpoint."""
    response = client.get("/api/prompts/debugging-assistant")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data


def test_get_nonexistent_prompt(client):
    """Test get nonexistent prompt."""
    response = client.get("/api/prompts/nonexistent")
    assert response.status_code == 404


def test_server_status(client):
    """Test server status endpoint."""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "cpu_percent" in data["data"]
    assert "memory_percent" in data["data"]
