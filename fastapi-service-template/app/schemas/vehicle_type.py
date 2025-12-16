from pydantic import BaseModel, ConfigDict
from typing import Optional


class VehicleTypeCreate(BaseModel):
    """Schema for creating a new vehicle type"""
    name: str
    max_weight_kg: Optional[float] = None
    payload_ton: Optional[float] = None
    max_volume_m3: Optional[float] = None
    volume_m3: Optional[float] = None
    length_m: Optional[float] = None
    width_m: Optional[float] = None
    height_m: Optional[float] = None
    diesel: Optional[bool] = False
    hybrid: Optional[bool] = False
    ev_van: Optional[bool] = False
    ev_charge_time: Optional[float] = None
    ev_range_km: Optional[float] = None
    ev_energy_kwh_per_km: Optional[float] = None
    average_speed_kmh: Optional[float] = None
    fuel_consumption_per_100km: Optional[float] = None
    diesel_l_per_km: Optional[float] = None
    emission_factor_kg_per_km: Optional[float] = None
    cost_per_km: Optional[float] = None
    diesel_cost_zar_per_km: Optional[float] = None
    ev_cost_zar_per_km_ac: Optional[float] = None
    ev_cost_zar_per_km_dc: Optional[float] = None
    daily_rental_cost: Optional[float] = None
    is_active: Optional[bool] = True
    description: Optional[str] = None


class VehicleTypeUpdate(BaseModel):
    """Schema for updating an existing vehicle type"""
    name: Optional[str] = None
    max_weight_kg: Optional[float] = None
    payload_ton: Optional[float] = None
    max_volume_m3: Optional[float] = None
    volume_m3: Optional[float] = None
    length_m: Optional[float] = None
    width_m: Optional[float] = None
    height_m: Optional[float] = None
    diesel: Optional[bool] = None
    hybrid: Optional[bool] = None
    ev_van: Optional[bool] = None
    ev_charge_time: Optional[float] = None
    ev_range_km: Optional[float] = None
    ev_energy_kwh_per_km: Optional[float] = None
    average_speed_kmh: Optional[float] = None
    fuel_consumption_per_100km: Optional[float] = None
    diesel_l_per_km: Optional[float] = None
    emission_factor_kg_per_km: Optional[float] = None
    cost_per_km: Optional[float] = None
    diesel_cost_zar_per_km: Optional[float] = None
    ev_cost_zar_per_km_ac: Optional[float] = None
    ev_cost_zar_per_km_dc: Optional[float] = None
    daily_rental_cost: Optional[float] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None


class VehicleTypeResponse(BaseModel):
    """Schema for vehicle type response"""
    id: int
    name: str
    max_weight_kg: Optional[float] = None
    payload_ton: Optional[float] = None
    max_volume_m3: Optional[float] = None
    volume_m3: Optional[float] = None
    length_m: Optional[float] = None
    width_m: Optional[float] = None
    height_m: Optional[float] = None
    diesel: Optional[bool] = False
    hybrid: Optional[bool] = False
    ev_van: Optional[bool] = False
    ev_charge_time: Optional[float] = None
    ev_range_km: Optional[float] = None
    ev_energy_kwh_per_km: Optional[float] = None
    average_speed_kmh: Optional[float] = None
    fuel_consumption_per_100km: Optional[float] = None
    diesel_l_per_km: Optional[float] = None
    emission_factor_kg_per_km: Optional[float] = None
    cost_per_km: Optional[float] = None
    diesel_cost_zar_per_km: Optional[float] = None
    ev_cost_zar_per_km_ac: Optional[float] = None
    ev_cost_zar_per_km_dc: Optional[float] = None
    daily_rental_cost: Optional[float] = None
    is_active: bool
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
