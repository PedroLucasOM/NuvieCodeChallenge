from sqlalchemy import Column, Integer, String, DateTime, Text, Date
from sqlalchemy.sql import func
from app.models.base import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    ssn = Column(String(11), unique=True, index=True)
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(10))
    phone = Column(String(20))
    email = Column(String(255))
    
    # Campos adicionais do Synthea
    synthea_id = Column(String(255), unique=True, index=True)
    race = Column(String(50))
    ethnicity = Column(String(50))
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
