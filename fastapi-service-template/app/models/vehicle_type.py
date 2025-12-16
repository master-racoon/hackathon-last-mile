from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base


class VehicleType(Base):
    """Vehicle Type model for different types of vehicles used in shipping"""
    __tablename__ = "vehicle_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    capacity_kg = Column(Float, nullable=True, comment="Maximum weight capacity in kg")
    capacity_m3 = Column(Float, nullable=True, comment="Maximum volume capacity in cubic meters")
    
    def __repr__(self):
        return f"<VehicleType(id={self.id}, name='{self.name}', code='{self.code}')>"
