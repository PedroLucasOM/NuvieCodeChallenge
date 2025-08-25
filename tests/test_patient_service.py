import pytest
from datetime import date
from app.application.use_cases.patient_use_cases import PatientUseCases
from app.infrastructure.repositories.patient_repository import PatientRepository

@pytest.mark.asyncio
async def test_create_patient(db_session):
    patient_repository = PatientRepository(db_session)
    patient_use_cases = PatientUseCases(patient_repository)
    
    patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": date(1990, 1, 15),
        "gender": "male",
        "email": "john.doe@example.com"
    }
    
    patient = await patient_use_cases.create_patient(patient_data)
    
    assert patient.id is not None
    assert patient.first_name == "John"
    assert patient.last_name == "Doe"
    assert patient.email == "john.doe@example.com"

@pytest.mark.asyncio
async def test_get_patient_by_id(db_session):
    patient_repository = PatientRepository(db_session)
    patient_use_cases = PatientUseCases(patient_repository)
    
    patient_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "date_of_birth": date(1985, 5, 20),
        "gender": "female"
    }
    
    created_patient = await patient_use_cases.create_patient(patient_data)
    found_patient = await patient_use_cases.get_patient_by_id(created_patient.id)
    
    assert found_patient is not None
    assert found_patient.id == created_patient.id
    assert found_patient.first_name == "Jane"

@pytest.mark.asyncio
async def test_search_patients(db_session):
    patient_repository = PatientRepository(db_session)
    patient_use_cases = PatientUseCases(patient_repository)
    
    patients_data = [
        {
            "first_name": "Alice",
            "last_name": "Johnson",
            "date_of_birth": date(1990, 1, 1),
            "gender": "female"
        },
        {
            "first_name": "Bob",
            "last_name": "Wilson",
            "date_of_birth": date(1985, 1, 1),
            "gender": "male"
        },
        {
            "first_name": "Charlie",
            "last_name": "Brown",
            "date_of_birth": date(1988, 1, 1),
            "gender": "male"
        }
    ]
    
    for patient_data in patients_data:
        await patient_use_cases.create_patient(patient_data)
    
    results = await patient_use_cases.search_patients(search="Alice")
    assert len(results) == 1
    assert results[0].first_name == "Alice"
    
    all_results = await patient_use_cases.search_patients()
    assert len(all_results) >= 3
