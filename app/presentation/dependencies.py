from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas.user import User
from app.application.use_cases.auth_use_cases import AuthUseCases
from app.infrastructure.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        user_repository = UserRepository(db)
        auth_use_cases = AuthUseCases(user_repository)
        user = await auth_use_cases.get_user_by_token(token)
        
        if user is None:
            raise credentials_exception
        
        return User.from_orm(user)
    except Exception:
        raise credentials_exception
