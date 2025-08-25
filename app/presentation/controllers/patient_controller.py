from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas.patient import Patient, PatientCreate, PatientUpdate
from app.schemas.user import User
from app.application.use_cases.patient_use_cases import PatientUseCases
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.infrastructure.external.synthea_service import SyntheaService
from app.presentation.dependencies import get_current_user

router = APIRouter()

async def get_patient_use_cases(db: AsyncSession = Depends(get_db)) -> PatientUseCases:
    patient_repository = PatientRepository(db)
    return PatientUseCases(patient_repository)

@router.post("/", response_model=Patient)
async def create_patient(
    patient: PatientCreate,
    patient_use_cases: PatientUseCases = Depends(get_patient_use_cases),
    current_user: User = Depends(get_current_user)
):
    try:
        patient_entity = await patient_use_cases.create_patient(patient.dict())
        return Patient.from_orm(patient_entity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[Patient])
async def read_patients(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    search: Optional[str] = Query(None, description="Buscar por nome, email ou SSN"),
    gender: Optional[str] = Query(None, description="Filtrar por gênero"),
    city: Optional[str] = Query(None, description="Filtrar por cidade"),
    state: Optional[str] = Query(None, description="Filtrar por estado"),
    age_min: Optional[int] = Query(None, ge=0, le=150, description="Idade mínima"),
    age_max: Optional[int] = Query(None, ge=0, le=150, description="Idade máxima"),
    patient_use_cases: PatientUseCases = Depends(get_patient_use_cases),
    current_user: User = Depends(get_current_user)
):
    patients = await patient_use_cases.search_patients(
        search=search,
        gender=gender,
        city=city,
        state=state,
        age_min=age_min,
        age_max=age_max,
        skip=skip,
        limit=limit
    )
    return [Patient.from_orm(patient) for patient in patients]

@router.get("/{patient_id}", response_model=Patient)
async def read_patient(
    patient_id: int,
    patient_use_cases: PatientUseCases = Depends(get_patient_use_cases),
    current_user: User = Depends(get_current_user)
):
    patient = await patient_use_cases.get_patient_by_id(patient_id)
    
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return Patient.from_orm(patient)

@router.put("/{patient_id}", response_model=Patient)
async def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    patient_use_cases: PatientUseCases = Depends(get_patient_use_cases),
    current_user: User = Depends(get_current_user)
):
    try:
        patient = await patient_use_cases.update_patient(
            patient_id, 
            patient_update.dict(exclude_unset=True)
        )
        
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente não encontrado"
            )
        
        return Patient.from_orm(patient)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: int,
    patient_use_cases: PatientUseCases = Depends(get_patient_use_cases),
    current_user: User = Depends(get_current_user)
):
    success = await patient_use_cases.delete_patient(patient_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return {"message": "Paciente deletado com sucesso"}

@router.post("/import-synthea")
async def import_synthea_data(
    count: int = Query(10, ge=1, le=100, description="Número de pacientes para importar"),
    patient_use_cases: PatientUseCases = Depends(get_patient_use_cases),
    current_user: User = Depends(get_current_user)
):
    synthea_service = SyntheaService()
    
    try:
        fhir_patients = await synthea_service.fetch_patients(count)
        imported_count = 0
        
        for fhir_data in fhir_patients:
            patient_entity = await synthea_service.transform_fhir_to_patient(fhir_data)
            
            existing_patient = await patient_use_cases._patient_repository.get_by_synthea_id(
                patient_entity.synthea_id
            )
            
            if not existing_patient:
                await patient_use_cases.create_patient(patient_entity.__dict__)
                imported_count += 1
        
        return {
            "message": f"Importados {imported_count} pacientes do Synthea com sucesso",
            "imported_count": imported_count,
            "total_processed": len(fhir_patients)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao importar dados do Synthea: {str(e)}"
        )
