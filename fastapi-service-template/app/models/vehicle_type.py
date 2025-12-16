from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class VehicleType(Base):
    """Vehicle Type model for tracking different types of delivery vehicles"""
    __tablename__ = "vehicle_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True, comment="Vehicle type name (e.g., '8 TONNER', '12 TONNER')")
    
    # Capacity specifications
    max_weight_kg = Column(Float, nullable=True, comment="Maximum weight capacity in kilograms")
    payload_ton = Column(Float, nullable=True, comment="Payload capacity in tons")
    max_volume_m3 = Column(Float, nullable=True, comment="Maximum volume capacity in cubic meters")
    volume_m3 = Column(Float, nullable=True, comment="Volume in cubic meters")
    
    # Physical dimensions
    length_m = Column(Float, nullable=True, comment="Length in meters")
    width_m = Column(Float, nullable=True, comment="Width in meters")
    height_m = Column(Float, nullable=True, comment="Height in meters")
    
    # Vehicle type flags
    diesel = Column(Boolean, default=False, nullable=True, comment="Whether this is a diesel vehicle")
    hybrid = Column(Boolean, default=False, nullable=True, comment="Whether this is a hybrid vehicle")
    ev_van = Column(Boolean, default=False, nullable=True, comment="Whether this is an electric van")
    
    # EV specifications
    ev_charge_time = Column(Float, nullable=True, comment="EV charging time in hours")
    ev_range_km = Column(Float, nullable=True, comment="EV range in kilometers")
    ev_energy_kwh_per_km = Column(Float, nullable=True, comment="EV energy consumption in kWh per km")
    
    # Operational characteristics
    average_speed_kmh = Column(Float, nullable=True, comment="Average speed in km/h")
    fuel_consumption_per_100km = Column(Float, nullable=True, comment="Fuel consumption per 100km")
    diesel_l_per_km = Column(Float, nullable=True, comment="Diesel consumption in liters per km")
    
    # Cost and availability
    cost_per_km = Column(Float, nullable=True, comment="Operating cost per kilometer")
    diesel_cost_zar_per_km = Column(Float, nullable=True, comment="Diesel operating cost in ZAR per km")
    ev_cost_zar_per_km_ac = Column(Float, nullable=True, comment="EV operating cost in ZAR per km (AC charging)")
    ev_cost_zar_per_km_dc = Column(Float, nullable=True, comment="EV operating cost in ZAR per km (DC charging)")
    daily_rental_cost = Column(Float, nullable=True, comment="Daily rental cost")
    is_active = Column(Boolean, default=True, nullable=False, comment="Whether this vehicle type is currently available")
    
    # Additional information
    description = Column(Text, nullable=True, comment="Additional notes about this vehicle type")
    
    # Relationships
    customer_orders = relationship("CustomerOrder", back_populates="vehicle_type")
    
    def __repr__(self):
        return f"<VehicleType(id={self.id}, name='{self.name}', max_weight_kg={self.max_weight_kg})>"
