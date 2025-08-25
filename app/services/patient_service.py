from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
import httpx
from datetime import datetime

class PatientService:
    def __init__(self, db: Session):
        self.db = db

    def create_patient(self, patient: PatientCreate) -> Patient:
        """Criar um novo paciente"""
        db_patient = Patient(**patient.dict())
        self.db.add(db_patient)
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def get_patient(self, patient_id: int) -> Optional[Patient]:
        """Obter um paciente por ID"""
        return self.db.query(Patient).filter(Patient.id == patient_id).first()

    def get_patients(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Patient]:
        """Listar pacientes com paginação e busca"""
        query = self.db.query(Patient)
        
        if search:
            search_filter = or_(
                Patient.first_name.ilike(f"%{search}%"),
                Patient.last_name.ilike(f"%{search}%"),
                Patient.email.ilike(f"%{search}%"),
                Patient.ssn.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()

    def update_patient(self, patient_id: int, patient_update: PatientUpdate) -> Optional[Patient]:
        """Atualizar um paciente existente"""
        db_patient = self.get_patient(patient_id)
        
        if db_patient is None:
            return None
        
        update_data = patient_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_patient, field, value)
        
        db_patient.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_patient)
        
        return db_patient

    def delete_patient(self, patient_id: int) -> bool:
        """Deletar um paciente"""
        db_patient = self.get_patient(patient_id)
        
        if db_patient is None:
            return False
        
        self.db.delete(db_patient)
        self.db.commit()
        
        return True

    async def import_synthea_patients(self, count: int = 10) -> int:
        """Import patients from external API"""
        from app.infrastructure.external.synthea_service import SyntheaService
        
        synthea_service = SyntheaService()
        
        try:
            # Fetch FHIR data from external API
            fhir_patients = await synthea_service.fetch_patients(count)
            imported_count = 0
            
            for fhir_data in fhir_patients:
                # Transform FHIR data to Patient entity
                patient_entity = await synthea_service.transform_fhir_to_patient(fhir_data)
                
                # Check if patient already exists by external ID
                existing_patient = self.db.query(Patient).filter(
                    Patient.synthea_id == patient_entity.synthea_id
                ).first()
                
                if not existing_patient:
                    # Create PatientCreate from entity
                    patient_data = {
                        "first_name": patient_entity.first_name,
                        "last_name": patient_entity.last_name,
                        "date_of_birth": patient_entity.date_of_birth,
                        "gender": patient_entity.gender,
                        "ssn": patient_entity.ssn,
                        "address": patient_entity.address,
                        "city": patient_entity.city,
                        "state": patient_entity.state,
                        "zip_code": patient_entity.zip_code,
                        "phone": patient_entity.phone,
                        "email": patient_entity.email,
                        "race": patient_entity.race,
                        "ethnicity": patient_entity.ethnicity,
                        "synthea_id": patient_entity.synthea_id
                    }
                    
                    patient_create = PatientCreate(**patient_data)
                    self.create_patient(patient_create)
                    imported_count += 1
            
            return imported_count
            
        except Exception as e:
            raise Exception(f"Failed to import from external API: {str(e)}")
