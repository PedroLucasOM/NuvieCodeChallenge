from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, TokenData
from app.config import settings
from app.database.connection import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar senha"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Gerar hash da senha"""
        return pwd_context.hash(password)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Obter usuário por username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obter usuário por email"""
        return self.db.query(User).filter(User.email == email).first()

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Autenticar usuário"""
        user = self.get_user_by_username(username)
        
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        return user

    def create_user(self, user: UserCreate) -> User:
        """Criar novo usuário"""
        # Verificar se username já existe
        if self.get_user_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já está em uso"
            )
        
        # Verificar se email já existe
        if self.get_user_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
        
        hashed_password = self.get_password_hash(user.password)
        
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Criar token JWT"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        
        return encoded_jwt

    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
    ) -> User:
        """Obter usuário atual a partir do token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            
            if username is None:
                raise credentials_exception
            
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        
        auth_service = AuthService(db)
        user = auth_service.get_user_by_username(username=token_data.username)
        
        if user is None:
            raise credentials_exception
        
        return user
