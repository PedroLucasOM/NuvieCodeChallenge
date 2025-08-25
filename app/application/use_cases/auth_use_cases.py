from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.domain.entities.user import User
from app.domain.interfaces import IUserRepository
from app.config import settings

class AuthUseCases:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def register_user(self, user_data: Dict[str, Any]) -> User:
        existing_user = await self._user_repository.get_by_username(user_data["username"])
        if existing_user:
            raise ValueError("Username já está em uso")
        
        existing_email = await self._user_repository.get_by_email(user_data["email"])
        if existing_email:
            raise ValueError("Email já está em uso")
        
        hashed_password = self._hash_password(user_data["password"])
        
        user = User(
            id=None,
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hashed_password,
            full_name=user_data.get("full_name")
        )
        
        if not user.is_valid_for_creation():
            raise ValueError("Dados do usuário inválidos")
        
        return await self._user_repository.create(user)
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self._user_repository.get_by_username(username)
        
        if not user or not self._verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    async def get_user_by_token(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            
            if username is None:
                return None
            
            return await self._user_repository.get_by_username(username)
        except JWTError:
            return None
    
    def _hash_password(self, password: str) -> str:
        return self._pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)
