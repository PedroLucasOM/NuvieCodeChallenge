import pytest
from app.application.use_cases.patient_use_cases import PatientUseCases
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.infrastructure.external.external_api_service import ExternalApiService

@pytest.mark.asyncio
async def test_create_patient(db_session):
    patient_repository = PatientRepository(db_session)
    external_api_service = ExternalApiService()
    patient_use_cases = PatientUseCases(patient_repository, external_api_service)
    
    patient_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890"
    }
    
    patient = await patient_use_cases.create_patient(patient_data)
    
    assert patient.id is not None
    assert patient.name == "John Doe"
    assert patient.email == "john.doe@example.com"
    assert patient.phone == "+1234567890"

@pytest.mark.asyncio
async def test_get_patient_by_id(db_session):
    patient_repository = PatientRepository(db_session)
    external_api_service = ExternalApiService()
    patient_use_cases = PatientUseCases(patient_repository, external_api_service)
    
    patient_data = {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "phone": "+0987654321"
    }
    
    created_patient = await patient_use_cases.create_patient(patient_data)
    found_patient = await patient_use_cases.get_patient_by_id(created_patient.id)
    
    assert found_patient is not None
    assert found_patient.id == created_patient.id
    assert found_patient.name == "Jane Smith"

@pytest.mark.asyncio
async def test_get_patients_with_search(db_session):
    patient_repository = PatientRepository(db_session)
    external_api_service = ExternalApiService()
    patient_use_cases = PatientUseCases(patient_repository, external_api_service)
    
    patients_data = [
        {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "phone": "+1111111111"
        },
        {
            "name": "Bob Wilson",
            "email": "bob.wilson@example.com",
            "phone": "+2222222222"
        },
        {
            "name": "Charlie Brown",
            "email": "charlie.brown@example.com",
            "phone": "+3333333333"
        }
    ]
    
    for patient_data in patients_data:
        await patient_use_cases.create_patient(patient_data)
    
    results = await patient_use_cases.get_patients(search="Alice")
    assert len(results) >= 1
    assert any("Alice" in patient.name for patient in results)
    
    all_results = await patient_use_cases.get_patients()
    assert len(all_results) >= 3

@pytest.mark.asyncio
async def test_create_duplicate_email(db_session):
    patient_repository = PatientRepository(db_session)
    external_api_service = ExternalApiService()
    patient_use_cases = PatientUseCases(patient_repository, external_api_service)
    
    patient_data = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "phone": "+1234567890"
    }
    
    await patient_use_cases.create_patient(patient_data)
    
    with pytest.raises(ValueError, match="email already exists"):
        await patient_use_cases.create_patient(patient_data)
