from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime
from .vehicle_type import VehicleTypeResponse
from .order_prediction import OrderPredictionResponse


class CustomerOrderCreate(BaseModel):
    """Schema for creating a new customer order"""
    order_number: str
    customer_name: Optional[str] = None
    customer_reference: Optional[str] = None
    requested_delivery_date: date
    confirmation_number: Optional[str] = None
    vehicle_type_id: Optional[int] = None
    lead_time_days: Optional[int] = None
    load_date: Optional[date] = None
    estimated_arrival: Optional[date] = None
    origin_city: Optional[str] = None
    origin_country: Optional[str] = None
    destination_city: Optional[str] = None
    destination_country: Optional[str] = None
    weight_kg: Optional[float] = None
    volume_m3: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = "pending"


class CustomerOrderUpdate(BaseModel):
    """Schema for updating an existing customer order"""
    customer_name: Optional[str] = None
    customer_reference: Optional[str] = None
    requested_delivery_date: Optional[date] = None
    confirmation_number: Optional[str] = None
    vehicle_type_id: Optional[int] = None
    lead_time_days: Optional[int] = None
    load_date: Optional[date] = None
    estimated_arrival: Optional[date] = None
    origin_city: Optional[str] = None
    origin_country: Optional[str] = None
    destination_city: Optional[str] = None
    destination_country: Optional[str] = None
    weight_kg: Optional[float] = None
    volume_m3: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class CustomerOrderResponse(BaseModel):
    """Schema for customer order response"""
    id: int
    order_number: str
    customer_name: Optional[str] = None
    customer_reference: Optional[str] = None
    requested_delivery_date: date
    confirmation_number: Optional[str] = None
    vehicle_type_id: Optional[int] = None
    vehicle_type: Optional[VehicleTypeResponse] = None
    lead_time_days: Optional[int] = None
    load_date: Optional[date] = None
    estimated_arrival: Optional[date] = None
    origin_city: Optional[str] = None
    origin_country: Optional[str] = None
    destination_city: Optional[str] = None
    destination_country: Optional[str] = None
    weight_kg: Optional[float] = None
    volume_m3: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_prediction: Optional[OrderPredictionResponse] = None

    model_config = ConfigDict(from_attributes=True)
