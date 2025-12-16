from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class OrderPrediction(Base):
    __tablename__ = "order_predictions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Link to the customer order
    order_id = Column(Integer, ForeignKey("customer_orders.id"), nullable=False, index=True)
    order = relationship("CustomerOrder", back_populates="predictions")
    
    # Link to the recommended vehicle type for this prediction
    recommended_vehicle_type_id = Column(Integer, ForeignKey("vehicle_types.id"), nullable=True, index=True)
    recommended_vehicle_type = relationship("VehicleType")
    
    # Link to the destination track (route) for this prediction
    destination_track_id = Column(Integer, ForeignKey("destination_tracks.id"), nullable=True, index=True, comment="Route used for this prediction")
    destination_track = relationship("DestinationTrack")
    
    # Prediction results
    predicted_delay_days = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<OrderPrediction(id={self.id}, order_id={self.order_id}, vehicle_id={self.recommended_vehicle_type_id}, track_id={self.destination_track_id})>"
