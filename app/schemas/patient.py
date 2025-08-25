from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    ssn: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    race: Optional[str] = None
    ethnicity: Optional[str] = None

class PatientCreate(PatientBase):
    synthea_id: Optional[str] = None

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    ssn: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    race: Optional[str] = None
    ethnicity: Optional[str] = None

class Patient(PatientBase):
    id: int
    synthea_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, entity):
        return cls(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            date_of_birth=entity.date_of_birth,
            gender=entity.gender,
            ssn=entity.ssn,
            address=entity.address,
            city=entity.city,
            state=entity.state,
            zip_code=entity.zip_code,
            phone=entity.phone,
            email=entity.email,
            synthea_id=entity.synthea_id,
            race=entity.race,
            ethnicity=entity.ethnicity,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
