from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class Patient:
    id: Optional[int]
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    ssn: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    synthea_id: Optional[str] = None
    race: Optional[str] = None
    ethnicity: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def is_valid_for_creation(self) -> bool:
        return bool(
            self.first_name and 
            self.last_name and 
            self.date_of_birth and 
            self.gender
        )
