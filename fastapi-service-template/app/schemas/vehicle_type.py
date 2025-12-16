from pydantic import BaseModel, ConfigDict
from typing import Optional


class VehicleTypeCreate(BaseModel):
    """Schema for creating a new vehicle type"""
    name: str
    code: str
    description: Optional[str] = None
    capacity_kg: Optional[float] = None
    capacity_m3: Optional[float] = None


class VehicleTypeResponse(BaseModel):
    """Schema for vehicle type response"""
    id: int
    name: str
    code: str
    description: Optional[str] = None
    capacity_kg: Optional[float] = None
    capacity_m3: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
