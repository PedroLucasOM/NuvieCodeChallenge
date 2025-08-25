import pytest
from fastapi.testclient import TestClient

class TestAuthEndpoints:
    
    def test_register_user_success(self, client):
        """Test successful user registration"""
        user_data = {
            "username": "testuser123",
            "email": "test@example.com",
            "password": "TestPass123!",
            "full_name": "Test User"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser123"
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"
        assert "id" in data
        assert "password" not in data

    def test_register_user_invalid_email(self, client):
        """Test registration with invalid email"""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "TestPass123!",
            "full_name": "Test User"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
        data = response.json()
        assert "error" in data and data["error"] == "Validation failed"

    def test_register_user_weak_password(self, client):
        """Test registration with weak password"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "weak",
            "full_name": "Test User"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
        data = response.json()
        assert "error" in data and data["error"] == "Validation failed"

    def test_register_user_invalid_username(self, client):
        """Test registration with invalid username characters"""
        user_data = {
            "username": "test@user",
            "email": "test@example.com", 
            "password": "TestPass123!",
            "full_name": "Test User"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400

    def test_login_success(self, client):
        """Test successful login"""
        user_data = {
            "username": "logintest",
            "email": "login@example.com",
            "password": "TestPass123!",
            "full_name": "Login Test"
        }
        client.post("/auth/register", json=user_data)
        
        login_data = {
            "username": "logintest",
            "password": "TestPass123!"
        }
        
        response = client.post("/auth/token", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        login_data = {
            "username": "nonexistent",
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/token", json=login_data)
        assert response.status_code == 401
        data = response.json()
        assert ("detail" in data and "invalid" in data["detail"].lower()) or \
               ("message" in data and "invalid" in data["message"].lower()) or \
               ("error" in data and "invalid" in str(data["error"]).lower())

    def test_get_current_user_unauthorized(self, client):
        response = client.get("/auth/me")
        assert response.status_code == 403

    def test_get_current_user_with_token(self, client):
        """Test accessing protected endpoint with valid token"""
        user_data = {
            "username": "tokentest",
            "email": "token@example.com",
            "password": "TestPass123!",
            "full_name": "Token Test"
        }
        client.post("/auth/register", json=user_data)
        
        login_response = client.post("/auth/token", json={
            "username": "tokentest",
            "password": "TestPass123!"
        })
        token = login_response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "tokentest"
