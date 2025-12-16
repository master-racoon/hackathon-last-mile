from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class CustomerOrder(Base):
    """Customer Order model for tracking shipment orders - based on open_orders.xlsx structure"""
    __tablename__ = "customer_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False, index=True)
    
    # Customer information
    customer_name = Column(String(255), nullable=True, comment="Customer Name from Excel")
    
    # Order details - from Excel
    requested_delivery_date = Column(Date, nullable=False, comment="Customer requested delivery date (YYYYMMDD format in Excel)")
    line_item_count = Column(Integer, nullable=True, comment="Number of line items aggregated for this order")
    
    # Origin information - from Excel columns: From Country, From stare (state)
    origin_country = Column(String(100), nullable=True, comment="From Country")
    origin_state = Column(String(100), nullable=True, comment="From stare (state) - origin state/region")
    
    # Destination information - from Excel columns: To country, To State
    destination_country = Column(String(100), nullable=True, comment="To country")
    destination_state = Column(String(100), nullable=True, comment="To State - destination state/region")
    
    # Cargo details - aggregated from line items
    gross_weight_kg = Column(Float, nullable=True, comment="Total gross weight aggregated from all line items")
    net_weight_kg = Column(Float, nullable=True, comment="Total net weight aggregated from all line items")
    total_width = Column(Float, nullable=True, comment="Total width aggregated from all line items")
    
    # Delivery method - from Excel (40 = 40ft container, 20 = 20ft container)
    delivery_method = Column(Integer, nullable=True, comment="Delivery method code from Excel (40=40ft, 20=20ft)")
    
    # Vehicle type mapping
    vehicle_type_id = Column(Integer, ForeignKey("vehicle_types.id"), nullable=True)
    vehicle_type = relationship("VehicleType", back_populates="customer_orders")
    
    # Predictions relationship - one order can have many predictions (different vehicle/track combinations)
    predictions = relationship("OrderPrediction", back_populates="order")
    
    # Calculated/predicted fields
    lead_time_days = Column(Integer, nullable=True, comment="Expected lead time in days")
    load_date = Column(Date, nullable=True, comment="Date when cargo is loaded")
    estimated_arrival = Column(Date, nullable=True, comment="Estimated arrival date")
    
    # Additional information
    notes = Column(Text, nullable=True)
    status = Column(String(50), nullable=True, default="pending", comment="Order status: pending, confirmed, in_transit, delivered, cancelled")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<CustomerOrder(id={self.id}, order_number='{self.order_number}', status='{self.status}')>"
