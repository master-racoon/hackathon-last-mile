from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class OrderPrediction(Base):
    __tablename__ = "order_predictions"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("customer_orders.id"), nullable=False, index=True)
    order = relationship("CustomerOrder")

    predicted_delay_days = Column(Float, nullable=True)
    recommended_vehicle_type_id = Column(Integer, ForeignKey("vehicle_types.id"), nullable=True)
    recommended_vehicle_type = relationship("VehicleType")
    confidence = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<OrderPrediction(id={self.id}, order_id={self.order_id}, predicted_delay={self.predicted_delay_days})>"
