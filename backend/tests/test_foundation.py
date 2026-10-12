import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

def test_app_configuration():
    """Verify core settings load properly."""
    assert settings.PROJECT_NAME is not None
    assert settings.API_V1_STR == "/api/v1"
    assert settings.DATABASE_NAME == "career_guidance_db"

def test_root_endpoint():
    """Verify root documentation and info endpoint."""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert data["health"] == "/api/v1/health"

def test_health_check_endpoint():
    """Verify system health endpoint and database ping."""
    with TestClient(app) as client:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "database_connected" in data

def test_openapi_docs_endpoint():
    """Verify OpenAPI schema generation."""
    with TestClient(app) as client:
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == settings.PROJECT_NAME
