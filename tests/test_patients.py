import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestPatientEndpoints:
    
    @pytest.fixture(autouse=True)
    def setup_auth(self):
        user_data = {
            "username": "patienttest",
            "email": "patient@example.com", 
            "password": "TestPass123!",
            "full_name": "Patient Test User"
        }
        register_response = client.post("/auth/register", json=user_data)
        
        self.token = None
        self.headers = {}
        
        if register_response.status_code == 201:
            login_response = client.post("/auth/token", json={
                "username": "patienttest",
                "password": "TestPass123!"
            })
            
            if login_response.status_code == 200:
                self.token = login_response.json()["access_token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_create_patient_success(self):
        if not self.token:
            pytest.skip("Authentication required but login failed")
            
        patient_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890"
        }
        
        response = client.post("/patients/", json=patient_data, headers=self.headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john.doe@example.com"
        assert "id" in data

    def test_create_patient_invalid_email(self):
        patient_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "phone": "+1234567890"
        }
        
        response = client.post("/patients/", json=patient_data, headers=self.headers)
        assert response.status_code == 400

    def test_create_patient_invalid_phone(self):
        patient_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "123"
        }
        
        response = client.post("/patients/", json=patient_data, headers=self.headers)
        assert response.status_code == 400

    def test_create_patient_duplicate_email(self):
        patient_data = {
            "name": "John Doe",
            "email": "duplicate@example.com",
            "phone": "+1234567890"
        }
        
        response1 = client.post("/patients/", json=patient_data, headers=self.headers)
        assert response1.status_code == 201
        
        response2 = client.post("/patients/", json=patient_data, headers=self.headers)
        assert response2.status_code == 400

    def test_get_patients_unauthorized(self):
        response = client.get("/patients/")
        assert response.status_code == 403

    def test_get_patients_with_auth(self):
        response = client.get("/patients/", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_patients_with_search(self):
        patient_data = {
            "name": "SearchTest User",
            "email": "searchtest@example.com",
            "phone": "+1234567890"
        }
        client.post("/patients/", json=patient_data, headers=self.headers)
        
        response = client.get("/patients/?search=SearchTest", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any("SearchTest" in patient["name"] for patient in data)

    def test_get_patients_with_pagination(self):
        response = client.get("/patients/?skip=0&limit=5", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5

    def test_get_patient_by_id(self):
        patient_data = {
            "name": "GetTest User",
            "email": "gettest@example.com",
            "phone": "+1234567890"
        }
        create_response = client.post("/patients/", json=patient_data, headers=self.headers)
        patient_id = create_response.json()["id"]
        
        response = client.get(f"/patients/{patient_id}", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == patient_id
        assert data["name"] == "GetTest User"

    def test_get_nonexistent_patient(self):
        response = client.get("/patients/99999", headers=self.headers)
        assert response.status_code == 404

    def test_update_patient(self):
        patient_data = {
            "name": "UpdateTest User",
            "email": "updatetest@example.com",
            "phone": "+1234567890"
        }
        create_response = client.post("/patients/", json=patient_data, headers=self.headers)
        patient_id = create_response.json()["id"]
        
        update_data = {
            "name": "Updated Name",
            "phone": "+0987654321"
        }
        response = client.put(f"/patients/{patient_id}", json=update_data, headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["phone"] == "+0987654321"
        assert data["email"] == "updatetest@example.com"

    def test_delete_patient(self):
        patient_data = {
            "name": "DeleteTest User",
            "email": "deletetest@example.com",
            "phone": "+1234567890"
        }
        create_response = client.post("/patients/", json=patient_data, headers=self.headers)
        patient_id = create_response.json()["id"]
        
        response = client.delete(f"/patients/{patient_id}", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert "deleted" in data["message"].lower()
        
        get_response = client.get(f"/patients/{patient_id}", headers=self.headers)
        assert get_response.status_code == 404

    def test_import_external_data(self):
        response = client.post("/patients/import-data?count=3", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert "imported" in data["message"].lower()
