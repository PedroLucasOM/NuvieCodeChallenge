from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.domain.entities.patient import Patient
from app.domain.entities.user import User

class IPatientRepository(ABC):
    @abstractmethod
    async def create(self, patient: Patient) -> Patient:
        pass
    
    @abstractmethod
    async def get_by_id(self, patient_id: int) -> Optional[Patient]:
        pass
    
    @abstractmethod
    async def get_by_synthea_id(self, synthea_id: str) -> Optional[Patient]:
        pass
    
    @abstractmethod
    async def find_many(self, filters: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[Patient]:
        pass
    
    @abstractmethod
    async def update(self, patient_id: int, patient_data: Dict[str, Any]) -> Optional[Patient]:
        pass
    
    @abstractmethod
    async def delete(self, patient_id: int) -> bool:
        pass

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

class ISyntheaService(ABC):
    @abstractmethod
    async def fetch_patients(self, count: int = 10) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def transform_fhir_to_patient(self, fhir_data: Dict[str, Any]) -> Patient:
        pass
