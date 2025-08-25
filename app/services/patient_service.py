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

    async def import_synthea_patients(self) -> int:
        """Importar pacientes do Synthea (simulação)"""
        # Esta é uma implementação simulada
        # Em um cenário real, você faria requisições para a API do Synthea
        
        synthea_patients = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-01-15",
                "gender": "male",
                "synthea_id": "synthea_001",
                "race": "white",
                "ethnicity": "non-hispanic"
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "date_of_birth": "1985-05-20",
                "gender": "female",
                "synthea_id": "synthea_002",
                "race": "black",
                "ethnicity": "non-hispanic"
            }
        ]
        
        imported_count = 0
        
        for patient_data in synthea_patients:
            # Verificar se o paciente já existe
            existing_patient = self.db.query(Patient).filter(
                Patient.synthea_id == patient_data["synthea_id"]
            ).first()
            
            if not existing_patient:
                patient_create = PatientCreate(**patient_data)
                self.create_patient(patient_create)
                imported_count += 1
        
        return imported_count
