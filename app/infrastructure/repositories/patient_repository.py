from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from datetime import datetime, date
from app.domain.entities.patient import Patient as PatientEntity
from app.domain.interfaces import IPatientRepository
from app.models.patient import Patient as PatientModel

class PatientRepository(IPatientRepository):
    def __init__(self, db: AsyncSession):
        self._db = db
    
    async def create(self, patient: PatientEntity) -> PatientEntity:
        db_patient = PatientModel(
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=patient.date_of_birth,
            gender=patient.gender,
            ssn=patient.ssn,
            address=patient.address,
            city=patient.city,
            state=patient.state,
            zip_code=patient.zip_code,
            phone=patient.phone,
            email=patient.email,
            synthea_id=patient.synthea_id,
            race=patient.race,
            ethnicity=patient.ethnicity
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
    
    async def get_by_synthea_id(self, synthea_id: str) -> Optional[PatientEntity]:
        result = await self._db.execute(
            select(PatientModel).where(PatientModel.synthea_id == synthea_id)
        )
        db_patient = result.scalar_one_or_none()
        
        return self._to_entity(db_patient) if db_patient else None
    
    async def find_many(self, filters: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[PatientEntity]:
        query = select(PatientModel)
        
        conditions = []
        
        if "search" in filters:
            search_term = f"%{filters['search']}%"
            conditions.append(
                or_(
                    PatientModel.first_name.ilike(search_term),
                    PatientModel.last_name.ilike(search_term),
                    PatientModel.email.ilike(search_term),
                    PatientModel.ssn.ilike(search_term)
                )
            )
        
        if "gender" in filters:
            conditions.append(PatientModel.gender == filters["gender"])
        
        if "city" in filters:
            conditions.append(PatientModel.city.ilike(f"%{filters['city']}%"))
        
        if "state" in filters:
            conditions.append(PatientModel.state.ilike(f"%{filters['state']}%"))
        
        if "age_min" in filters or "age_max" in filters:
            today = date.today()
            if "age_min" in filters:
                max_birth_date = date(today.year - filters["age_min"], today.month, today.day)
                conditions.append(PatientModel.date_of_birth <= max_birth_date)
            if "age_max" in filters:
                min_birth_date = date(today.year - filters["age_max"] - 1, today.month, today.day)
                conditions.append(PatientModel.date_of_birth > min_birth_date)
        
        if conditions:
            query = query.where(and_(*conditions))
        
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
            first_name=db_patient.first_name,
            last_name=db_patient.last_name,
            date_of_birth=db_patient.date_of_birth,
            gender=db_patient.gender,
            ssn=db_patient.ssn,
            address=db_patient.address,
            city=db_patient.city,
            state=db_patient.state,
            zip_code=db_patient.zip_code,
            phone=db_patient.phone,
            email=db_patient.email,
            synthea_id=db_patient.synthea_id,
            race=db_patient.race,
            ethnicity=db_patient.ethnicity,
            created_at=db_patient.created_at,
            updated_at=db_patient.updated_at
        )
