from typing import List, Optional, Dict, Any
from app.domain.entities.patient import Patient
from app.domain.interfaces import IPatientRepository
from app.infrastructure.external.external_api_service import ExternalApiService

class PatientUseCases:
    def __init__(self, patient_repository: IPatientRepository, external_api_service: ExternalApiService = None):
        self._patient_repository = patient_repository
        self._external_api_service = external_api_service or ExternalApiService()
    
    async def create_patient(self, patient_data: Dict[str, Any]) -> Patient:
        patient = Patient(
            id=None,
            name=patient_data["name"],
            email=patient_data["email"],
            phone=patient_data["phone"]
        )
        
        if not patient.is_valid_for_creation():
            raise ValueError("Invalid patient data")
        
        existing_patient = await self._patient_repository.get_by_email(patient.email)
        if existing_patient:
            raise ValueError("Patient with this email already exists")
        
        return await self._patient_repository.create(patient)
    
    async def get_patient_by_id(self, patient_id: int) -> Optional[Patient]:
        return await self._patient_repository.get_by_id(patient_id)
    
    async def get_patients(
        self, 
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Patient]:
        return await self._patient_repository.get_patients(skip, limit, search)
    
    async def update_patient(self, patient_id: int, update_data: Dict[str, Any]) -> Optional[Patient]:
        if "email" in update_data:
            existing_patient = await self._patient_repository.get_by_email(update_data["email"])
            if existing_patient and existing_patient.id != patient_id:
                raise ValueError("Patient with this email already exists")
        
        return await self._patient_repository.update(patient_id, update_data)
    
    async def delete_patient(self, patient_id: int) -> bool:
        return await self._patient_repository.delete(patient_id)
    
    async def import_external_patients(self, count: int = 10) -> int:
        external_patients = await self._external_api_service.fetch_patients(count)
        imported_count = 0
        
        for patient_data in external_patients:
            try:
                existing_patient = await self._patient_repository.get_by_email(patient_data["email"])
                if not existing_patient:
                    await self.create_patient(patient_data)
                    imported_count += 1
            except Exception:
                continue
        
        return imported_count
