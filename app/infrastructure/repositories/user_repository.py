from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.entities.user import User as UserEntity
from app.domain.interfaces import IUserRepository
from app.models.user import User as UserModel

class UserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self._db = db
    
    async def create(self, user: UserEntity) -> UserEntity:
        db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser
        )
        
        self._db.add(db_user)
        await self._db.commit()
        await self._db.refresh(db_user)
        
        return self._to_entity(db_user)
    
    async def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        result = await self._db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        db_user = result.scalar_one_or_none()
        
        return self._to_entity(db_user) if db_user else None
    
    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        result = await self._db.execute(
            select(UserModel).where(UserModel.username == username)
        )
        db_user = result.scalar_one_or_none()
        
        return self._to_entity(db_user) if db_user else None
    
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        result = await self._db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_user = result.scalar_one_or_none()
        
        return self._to_entity(db_user) if db_user else None
    
    def _to_entity(self, db_user: UserModel) -> UserEntity:
        return UserEntity(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            full_name=db_user.full_name,
            is_active=db_user.is_active,
            is_superuser=db_user.is_superuser,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
