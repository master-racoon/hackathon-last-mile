from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class OrderPredictionResponse(BaseModel):
    id: int
    order_id: int
    predicted_delay_days: Optional[float] = None
    recommended_vehicle_type_id: Optional[int] = None
    destination_track_id: Optional[int] = None
    confidence: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderPredictionCreate(BaseModel):
    order_id: int
    predicted_delay_days: Optional[float] = None
    recommended_vehicle_type_id: Optional[int] = None
    destination_track_id: Optional[int] = None
    confidence: Optional[float] = None
