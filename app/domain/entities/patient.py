from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Patient:
    id: Optional[int]
    name: str
    email: str
    phone: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def is_valid_for_creation(self) -> bool:
        return bool(
            self.name and 
            self.email and 
            self.phone
        )
