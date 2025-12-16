from sqlalchemy.orm import Session
from typing import List, Optional
from models.vehicle_type import VehicleType
from schemas.vehicle_type import VehicleTypeCreate, VehicleTypeUpdate


class VehicleTypeRepository:
    """Repository for vehicle type database operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[VehicleType]:
        """Get all vehicle types with pagination"""
        query = self.db.query(VehicleType)
        if active_only:
            query = query.filter(VehicleType.is_active == True)
        return query.offset(skip).limit(limit).all()

    def get_by_id(self, vehicle_type_id: int) -> Optional[VehicleType]:
        """Get a vehicle type by ID"""
        return self.db.query(VehicleType).filter(VehicleType.id == vehicle_type_id).first()

    def get_by_name(self, name: str) -> Optional[VehicleType]:
        """Get a vehicle type by name"""
        return self.db.query(VehicleType).filter(VehicleType.name == name).first()

    def create(self, vehicle_type: VehicleTypeCreate) -> VehicleType:
        """Create a new vehicle type"""
        db_vehicle_type = VehicleType(**vehicle_type.model_dump())
        self.db.add(db_vehicle_type)
        self.db.commit()
        self.db.refresh(db_vehicle_type)
        return db_vehicle_type

    def update(self, vehicle_type_id: int, vehicle_type_update: VehicleTypeUpdate) -> Optional[VehicleType]:
        """Update an existing vehicle type"""
        db_vehicle_type = self.get_by_id(vehicle_type_id)
        if not db_vehicle_type:
            return None

        update_data = vehicle_type_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vehicle_type, field, value)

        self.db.commit()
        self.db.refresh(db_vehicle_type)
        return db_vehicle_type

    def delete(self, vehicle_type_id: int) -> bool:
        """Delete a vehicle type"""
        db_vehicle_type = self.get_by_id(vehicle_type_id)
        if not db_vehicle_type:
            return False

        self.db.delete(db_vehicle_type)
        self.db.commit()
        return True

    def get_by_capacity(
        self, 
        min_weight_kg: Optional[float] = None,
        min_volume_m3: Optional[float] = None
    ) -> List[VehicleType]:
        """Get vehicle types that meet minimum capacity requirements"""
        query = self.db.query(VehicleType).filter(VehicleType.is_active == True)
        
        if min_weight_kg is not None:
            query = query.filter(VehicleType.max_weight_kg >= min_weight_kg)
        
        if min_volume_m3 is not None:
            query = query.filter(VehicleType.max_volume_m3 >= min_volume_m3)
        
        return query.order_by(VehicleType.max_weight_kg).all()
