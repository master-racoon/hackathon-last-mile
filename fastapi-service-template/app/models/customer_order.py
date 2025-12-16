from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class CustomerOrder(Base):
    """Customer Order model for tracking shipment orders"""
    __tablename__ = "customer_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False, index=True)
    
    # Customer information
    customer_name = Column(String(255), nullable=True)
    customer_reference = Column(String(100), nullable=True)
    
    # Order details
    requested_delivery_date = Column(Date, nullable=False, comment="Customer requested delivery date")
    confirmation_number = Column(String(100), nullable=True, index=True, comment="Order confirmation number")
    
    # Vehicle and shipping details
    vehicle_type_id = Column(Integer, ForeignKey("vehicle_types.id"), nullable=True)
    vehicle_type = relationship("VehicleType")
    
    lead_time_days = Column(Integer, nullable=True, comment="Expected lead time in days")
    load_date = Column(Date, nullable=True, comment="Date when cargo is loaded")
    estimated_arrival = Column(Date, nullable=True, comment="Estimated arrival date")
    
    # Shipment details
    origin_city = Column(String(100), nullable=True)
    origin_country = Column(String(100), nullable=True)
    destination_city = Column(String(100), nullable=True)
    destination_country = Column(String(100), nullable=True)
    
    # Cargo details
    weight_kg = Column(Float, nullable=True)
    volume_m3 = Column(Float, nullable=True)
    
    # Additional information
    notes = Column(Text, nullable=True)
    status = Column(String(50), nullable=True, default="pending", comment="Order status: pending, confirmed, in_transit, delivered, cancelled")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<CustomerOrder(id={self.id}, order_number='{self.order_number}', status='{self.status}')>"
