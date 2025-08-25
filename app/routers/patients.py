from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.schemas.patient import Patient, PatientCreate, PatientUpdate
from app.schemas.user import User
from app.services.patient_service import PatientService
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Create a new patient"""
    patient_service = PatientService(db)
    try:
        return patient_service.create_patient(patient)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[Patient])
async def read_patients(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros para retornar"),
    search: Optional[str] = Query(None, description="Buscar por nome, email ou SSN"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Listar pacientes com paginação e busca"""
    patient_service = PatientService(db)
    return patient_service.get_patients(skip=skip, limit=limit, search=search)

@router.get("/{patient_id}", response_model=Patient)
async def read_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Obter um paciente específico por ID"""
    patient_service = PatientService(db)
    patient = patient_service.get_patient(patient_id)
    
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return patient

@router.put("/{patient_id}", response_model=Patient)
async def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Atualizar um paciente existente"""
    patient_service = PatientService(db)
    patient = patient_service.update_patient(patient_id, patient_update)
    
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return patient

@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Deletar um paciente"""
    patient_service = PatientService(db)
    success = patient_service.delete_patient(patient_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return {"message": "Paciente deletado com sucesso"}

@router.post("/import-synthea")
async def import_synthea_data(
    count: int = Query(10, ge=1, le=100, description="Number of patients to import"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Import patient data from external API"""
    patient_service = PatientService(db)
    try:
        imported_count = await patient_service.import_synthea_patients(count)
        return {
            "message": f"Successfully imported {imported_count} patients from external API",
            "imported_count": imported_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import external data: {str(e)}"
        )
