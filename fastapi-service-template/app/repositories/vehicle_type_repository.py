from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from models.vehicle_type import VehicleType
from schemas.vehicle_type import VehicleTypeCreate

logger = logging.getLogger(__name__)


class VehicleTypeRepository:
    """Repository for vehicle type database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[VehicleType]:
        """Get all vehicle types"""
        return self.db.query(VehicleType).all()
    
    def get_by_id(self, vehicle_type_id: int) -> Optional[VehicleType]:
        """Get a vehicle type by ID"""
        return self.db.query(VehicleType).filter(VehicleType.id == vehicle_type_id).first()
    
    def get_by_code(self, code: str) -> Optional[VehicleType]:
        """Get a vehicle type by code"""
        return self.db.query(VehicleType).filter(VehicleType.code == code).first()
    
    def create(self, vehicle_type_data: VehicleTypeCreate) -> VehicleType:
        """Create a new vehicle type"""
        db_vehicle_type = VehicleType(**vehicle_type_data.model_dump())
        self.db.add(db_vehicle_type)
        self.db.commit()
        self.db.refresh(db_vehicle_type)
        logger.info(f"Created vehicle type: {db_vehicle_type.name}")
        return db_vehicle_type
    
    def delete(self, vehicle_type_id: int) -> bool:
        """Delete a vehicle type"""
        vehicle_type = self.get_by_id(vehicle_type_id)
        if vehicle_type:
            self.db.delete(vehicle_type)
            self.db.commit()
            logger.info(f"Deleted vehicle type ID: {vehicle_type_id}")
            return True
        return False
