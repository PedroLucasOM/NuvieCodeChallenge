from typing import List, Optional, Dict, Any
from app.domain.entities.patient import Patient
from app.domain.interfaces import IPatientRepository

class PatientUseCases:
    def __init__(self, patient_repository: IPatientRepository):
        self._patient_repository = patient_repository
    
    async def create_patient(self, patient_data: Dict[str, Any]) -> Patient:
        patient = Patient(
            id=None,
            first_name=patient_data["first_name"],
            last_name=patient_data["last_name"],
            date_of_birth=patient_data["date_of_birth"],
            gender=patient_data["gender"],
            ssn=patient_data.get("ssn"),
            address=patient_data.get("address"),
            city=patient_data.get("city"),
            state=patient_data.get("state"),
            zip_code=patient_data.get("zip_code"),
            phone=patient_data.get("phone"),
            email=patient_data.get("email"),
            synthea_id=patient_data.get("synthea_id"),
            race=patient_data.get("race"),
            ethnicity=patient_data.get("ethnicity")
        )
        
        if not patient.is_valid_for_creation():
            raise ValueError("Dados do paciente inválidos")
        
        return await self._patient_repository.create(patient)
    
    async def get_patient_by_id(self, patient_id: int) -> Optional[Patient]:
        return await self._patient_repository.get_by_id(patient_id)
    
    async def search_patients(
        self, 
        search: Optional[str] = None,
        gender: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        age_min: Optional[int] = None,
        age_max: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Patient]:
        filters = {}
        
        if search:
            filters["search"] = search
        if gender:
            filters["gender"] = gender
        if city:
            filters["city"] = city
        if state:
            filters["state"] = state
        if age_min:
            filters["age_min"] = age_min
        if age_max:
            filters["age_max"] = age_max
        
        return await self._patient_repository.find_many(filters, skip, limit)
    
    async def update_patient(self, patient_id: int, update_data: Dict[str, Any]) -> Optional[Patient]:
        return await self._patient_repository.update(patient_id, update_data)
    
    async def delete_patient(self, patient_id: int) -> bool:
        return await self._patient_repository.delete(patient_id)
