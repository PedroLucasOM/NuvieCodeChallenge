from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.database.connection import get_db
from app.schemas.user import Token, User, UserCreate
from app.application.use_cases.auth_use_cases import AuthUseCases
from app.infrastructure.repositories.user_repository import UserRepository
from app.presentation.dependencies import get_current_user
from app.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_auth_use_cases(db: AsyncSession = Depends(get_db)) -> AuthUseCases:
    user_repository = UserRepository(db)
    return AuthUseCases(user_repository)

@router.post("/register", response_model=User)
async def register_user(
    user: UserCreate,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    try:
        user_entity = await auth_use_cases.register_user(user.dict())
        return User.from_orm(user_entity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    user = await auth_use_cases.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_use_cases.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
