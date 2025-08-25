from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def is_valid_for_creation(self) -> bool:
        return bool(
            self.username and 
            self.email and 
            self.hashed_password
        )
