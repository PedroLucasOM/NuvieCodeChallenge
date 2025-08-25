from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.domain.entities.patient import Patient as PatientEntity
from app.domain.interfaces import IPatientRepository
from app.models.patient import Patient as PatientModel

class PatientRepository(IPatientRepository):
    def __init__(self, db: AsyncSession):
        self._db = db
    
    async def create(self, patient: PatientEntity) -> PatientEntity:
        db_patient = PatientModel(
            name=patient.name,
            email=patient.email,
            phone=patient.phone
        )
        
        self._db.add(db_patient)
        await self._db.commit()
        await self._db.refresh(db_patient)
        
        return self._to_entity(db_patient)
    
    async def get_by_id(self, patient_id: int) -> Optional[PatientEntity]:
        result = await self._db.execute(
            select(PatientModel).where(PatientModel.id == patient_id)
        )
        db_patient = result.scalar_one_or_none()
        
        return self._to_entity(db_patient) if db_patient else None
    
    async def get_by_email(self, email: str) -> Optional[PatientEntity]:
        result = await self._db.execute(
            select(PatientModel).where(PatientModel.email == email)
        )
        db_patient = result.scalar_one_or_none()
        
        return self._to_entity(db_patient) if db_patient else None
    
    async def get_patients(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[PatientEntity]:
        query = select(PatientModel)
        
        if search:
            query = query.where(PatientModel.name.ilike(f"%{search}%"))
        
        query = query.offset(skip).limit(limit).order_by(PatientModel.created_at.desc())
        result = await self._db.execute(query)
        db_patients = result.scalars().all()
        
        return [self._to_entity(db_patient) for db_patient in db_patients]
    
    async def update(self, patient_id: int, patient_data: Dict[str, Any]) -> Optional[PatientEntity]:
        result = await self._db.execute(
            select(PatientModel).where(PatientModel.id == patient_id)
        )
        db_patient = result.scalar_one_or_none()
        
        if not db_patient:
            return None
        
        for field, value in patient_data.items():
            if hasattr(db_patient, field) and value is not None:
                setattr(db_patient, field, value)
        
        db_patient.updated_at = datetime.utcnow()
        await self._db.commit()
        await self._db.refresh(db_patient)
        
        return self._to_entity(db_patient)
    
    async def delete(self, patient_id: int) -> bool:
        result = await self._db.execute(
            select(PatientModel).where(PatientModel.id == patient_id)
        )
        db_patient = result.scalar_one_or_none()
        
        if not db_patient:
            return False
        
        await self._db.delete(db_patient)
        await self._db.commit()
        
        return True
    
    def _to_entity(self, db_patient: PatientModel) -> PatientEntity:
        return PatientEntity(
            id=db_patient.id,
            name=db_patient.name,
            email=db_patient.email,
            phone=db_patient.phone,
            created_at=db_patient.created_at,
            updated_at=db_patient.updated_at
        )
