from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas.patient import Patient, PatientCreate, PatientUpdate
from app.schemas.user import User
from app.application.use_cases.patient_use_cases import PatientUseCases
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.infrastructure.external.external_api_service import ExternalApiService
from app.presentation.dependencies import get_current_user

router = APIRouter()

async def get_patient_use_cases(db: AsyncSession = Depends(get_db)) -> PatientUseCases:
    patient_repository = PatientRepository(db)
    external_api_service = ExternalApiService()
    return PatientUseCases(patient_repository, external_api_service)

@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient: PatientCreate,
    patient_use_cases: PatientUseCases = Depends(get_patient_use_cases),
    current_user: User = Depends(get_current_user)
):
    try:
        patient_entity = await patient_use_cases.create_patient(patient.model_dump())
        return Patient.model_validate(patient_entity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[Patient])
async def get_patients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, min_length=2, description="Search in patient names"),
    patient_use_cases: PatientUseCases = Depends(get_patient_use_cases),
    current_user: User = Depends(get_current_user)
):
    patients = await patient_use_cases.get_patients(skip=skip, limit=limit, search=search)
    return [Patient.model_validate(patient) for patient in patients]

@router.get("/{patient_id}", response_model=Patient)
async def get_patient(
    patient_id: int,
    patient_use_cases: PatientUseCases = Depends(get_patient_use_cases),
    current_user: User = Depends(get_current_user)
):
    patient = await patient_use_cases.get_patient_by_id(patient_id)
    
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return Patient.model_validate(patient)

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
            patient_update.model_dump(exclude_unset=True)
        )
        
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        return Patient.model_validate(patient)
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
            detail="Patient not found"
        )
    
    return {"message": "Patient deleted successfully"}

@router.post("/import-data", status_code=status.HTTP_200_OK)
async def import_patient_data(
    count: int = Query(10, ge=1, le=100, description="Number of patients to import"),
    patient_use_cases: PatientUseCases = Depends(get_patient_use_cases),
    current_user: User = Depends(get_current_user)
):
    try:
        imported_count = await patient_use_cases.import_external_patients(count)
        return {"message": f"Successfully imported {imported_count} patients from external API"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing data: {str(e)}"
        )
