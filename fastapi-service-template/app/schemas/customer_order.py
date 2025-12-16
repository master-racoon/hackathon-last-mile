from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime
from .vehicle_type import VehicleTypeResponse
from .order_prediction import OrderPredictionResponse


class CustomerOrderCreate(BaseModel):
    """Schema for creating a new customer order - aligned with Excel structure"""
    order_number: str
    customer_name: Optional[str] = None
    requested_delivery_date: date
    line_item_count: Optional[int] = None
    origin_country: Optional[str] = None
    origin_state: Optional[str] = None
    destination_country: Optional[str] = None
    destination_state: Optional[str] = None
    gross_weight_kg: Optional[float] = None
    net_weight_kg: Optional[float] = None
    total_width: Optional[float] = None
    delivery_method: Optional[int] = None
    vehicle_type_id: Optional[int] = None
    lead_time_days: Optional[int] = None
    load_date: Optional[date] = None
    estimated_arrival: Optional[date] = None
    notes: Optional[str] = None
    status: Optional[str] = "pending"


class CustomerOrderUpdate(BaseModel):
    """Schema for updating an existing customer order"""
    customer_name: Optional[str] = None
    requested_delivery_date: Optional[date] = None
    line_item_count: Optional[int] = None
    origin_country: Optional[str] = None
    origin_state: Optional[str] = None
    destination_country: Optional[str] = None
    destination_state: Optional[str] = None
    gross_weight_kg: Optional[float] = None
    net_weight_kg: Optional[float] = None
    total_width: Optional[float] = None
    delivery_method: Optional[int] = None
    vehicle_type_id: Optional[int] = None
    lead_time_days: Optional[int] = None
    load_date: Optional[date] = None
    estimated_arrival: Optional[date] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class CustomerOrderResponse(BaseModel):
    """Schema for customer order response"""
    id: int
    order_number: str
    customer_name: Optional[str] = None
    requested_delivery_date: date
    line_item_count: Optional[int] = None
    origin_country: Optional[str] = None
    origin_state: Optional[str] = None
    destination_country: Optional[str] = None
    destination_state: Optional[str] = None
    gross_weight_kg: Optional[float] = None
    net_weight_kg: Optional[float] = None
    total_width: Optional[float] = None
    delivery_method: Optional[int] = None
    vehicle_type_id: Optional[int] = None
    vehicle_type: Optional[VehicleTypeResponse] = None
    lead_time_days: Optional[int] = None
    load_date: Optional[date] = None
    estimated_arrival: Optional[date] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_prediction: Optional[OrderPredictionResponse] = None

    model_config = ConfigDict(from_attributes=True)
