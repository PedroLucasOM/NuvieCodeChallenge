import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestSystemEndpoints:
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "active"

    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "nuvie-backend"
        assert "version" in data

    def test_metrics_endpoint(self):
        """Test the metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "nuvie-backend"
        assert "uptime" in data
        assert "database" in data
        assert "memory_usage" in data

class TestValidationHandling:
    
    def test_validation_error_format(self):
        """Test that validation errors return proper format"""
        response = client.post("/auth/register", json={
            "username": "",
            "email": "not-an-email",
            "password": "123"
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "message" in data
        assert "details" in data
        assert isinstance(data["details"], list)

    def test_404_error_format(self):
        """Test that 404 errors return proper format"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "message" in data

class TestSecurity:
    
    def test_protected_endpoints_require_auth(self):
        """Test that protected endpoints require authentication"""
        protected_endpoints = [
            ("GET", "/auth/me"),
            ("GET", "/patients/"),
            ("POST", "/patients/"),
            ("POST", "/patients/import-data")
        ]
        
        for method, endpoint in protected_endpoints:
            if method == "GET":
                response = client.get(endpoint)
            elif method == "POST":
                response = client.post(endpoint, json={})
            
            assert response.status_code == 403, f"Endpoint {method} {endpoint} should require authentication"

    def test_invalid_token_rejected(self):
        """Test that invalid tokens are rejected"""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401
