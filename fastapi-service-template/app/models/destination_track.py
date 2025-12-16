from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base


class DestinationTrack(Base):
    """Destination Track model for route information (distances, locations, weather)"""
    __tablename__ = "destination_tracks"

    id = Column(Integer, primary_key=True, index=True)
    
    # Route information
    origin_country = Column(String(10), nullable=False, index=True, comment="Origin country code")
    origin_city = Column(String(100), nullable=False, index=True, comment="Origin city code/name")
    destination_country = Column(String(10), nullable=False, index=True, comment="Destination country code")
    destination_city = Column(String(100), nullable=False, index=True, comment="Destination city code/name")
    
    # Distance information
    distance_km = Column(Float, nullable=True, index=True, comment="Route distance in kilometers")
    
    # Average weather conditions for this route (aggregated from historical data)
    origin_temp_mean = Column(Float, nullable=True, comment="Average origin temperature (°C)")
    dest_temp_mean = Column(Float, nullable=True, comment="Average destination temperature (°C)")
    
    # Relationships - predictions use this route
    predictions = relationship("OrderPrediction", back_populates="destination_track")
    
    def __repr__(self):
        return f"<DestinationTrack(id={self.id}, {self.origin_city} ({self.origin_country}) -> {self.destination_city} ({self.destination_country}), {self.distance_km}km)>"
