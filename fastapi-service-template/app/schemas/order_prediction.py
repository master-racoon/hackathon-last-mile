from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date


class OrderPredictionResponse(BaseModel):
    id: int
    order_id: int
    expected_lead_time_days: Optional[float] = None
    predicted_co2_kg: Optional[float] = None
    recommended_vehicle_type_id: Optional[int] = None
    destination_track_id: Optional[int] = None
    confidence: Optional[float] = None
    recommended_booking_date: Optional[date] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderPredictionCreate(BaseModel):
    order_id: int
    expected_lead_time_days: Optional[float] = None
    predicted_co2_kg: Optional[float] = None
    recommended_vehicle_type_id: Optional[int] = None
    destination_track_id: Optional[int] = None
    confidence: Optional[float] = None
    recommended_booking_date: Optional[date] = None
