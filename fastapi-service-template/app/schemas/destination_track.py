from pydantic import BaseModel, ConfigDict
from typing import Optional


class DestinationTrackBase(BaseModel):
    """Base schema for destination track"""
    origin_country: str
    origin_city: str
    destination_country: str
    destination_city: str
    distance_km: Optional[float] = None
    origin_temp_mean: Optional[float] = None
    dest_temp_mean: Optional[float] = None


class DestinationTrackCreate(DestinationTrackBase):
    """Schema for creating a new destination track"""
    pass


class DestinationTrackUpdate(BaseModel):
    """Schema for updating an existing destination track"""
    origin_country: Optional[str] = None
    origin_city: Optional[str] = None
    destination_country: Optional[str] = None
    destination_city: Optional[str] = None
    distance_km: Optional[float] = None
    origin_temp_mean: Optional[float] = None
    dest_temp_mean: Optional[float] = None


class DestinationTrackResponse(DestinationTrackBase):
    """Schema for destination track response"""
    id: int

    model_config = ConfigDict(from_attributes=True)
