from pydantic import BaseModel, ConfigDict
from typing import Optional


class VehicleEmissionsCreate(BaseModel):
    """Schema for creating a new vehicle emissions record"""
    vehicle_type_id: int
    temp_min: float
    temp_max: float
    co2_per_km: float


class VehicleEmissionsUpdate(BaseModel):
    """Schema for updating an existing vehicle emissions record"""
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    co2_per_km: Optional[float] = None


class VehicleEmissionsResponse(BaseModel):
    """Schema for vehicle emissions response"""
    id: int
    vehicle_type_id: int
    temp_min: float
    temp_max: float
    co2_per_km: float

    model_config = ConfigDict(from_attributes=True)
