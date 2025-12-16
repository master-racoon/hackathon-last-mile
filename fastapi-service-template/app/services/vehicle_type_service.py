from sqlalchemy.orm import Session
from typing import List, Optional
from repositories.vehicle_type_repository import VehicleTypeRepository
from schemas.vehicle_type import VehicleTypeCreate, VehicleTypeUpdate, VehicleTypeResponse


class VehicleTypeService:
    """Service layer for vehicle type business logic"""

    def __init__(self, db: Session):
        self.repository = VehicleTypeRepository(db)

    def get_all_vehicle_types(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        active_only: bool = False
    ) -> List[VehicleTypeResponse]:
        """Get all vehicle types"""
        vehicle_types = self.repository.get_all(skip, limit, active_only)
        return [VehicleTypeResponse.model_validate(vt) for vt in vehicle_types]

    def get_vehicle_type_by_id(self, vehicle_type_id: int) -> Optional[VehicleTypeResponse]:
        """Get a vehicle type by ID"""
        vehicle_type = self.repository.get_by_id(vehicle_type_id)
        if vehicle_type:
            return VehicleTypeResponse.model_validate(vehicle_type)
        return None

    def get_vehicle_type_by_name(self, name: str) -> Optional[VehicleTypeResponse]:
        """Get a vehicle type by name"""
        vehicle_type = self.repository.get_by_name(name)
        if vehicle_type:
            return VehicleTypeResponse.model_validate(vehicle_type)
        return None

    def create_vehicle_type(self, vehicle_type: VehicleTypeCreate) -> VehicleTypeResponse:
        """Create a new vehicle type"""
        # Check if vehicle type with this name already exists
        existing = self.repository.get_by_name(vehicle_type.name)
        if existing:
            raise ValueError(f"Vehicle type with name '{vehicle_type.name}' already exists")
        
        db_vehicle_type = self.repository.create(vehicle_type)
        return VehicleTypeResponse.model_validate(db_vehicle_type)

    def update_vehicle_type(
        self, 
        vehicle_type_id: int, 
        vehicle_type_update: VehicleTypeUpdate
    ) -> Optional[VehicleTypeResponse]:
        """Update an existing vehicle type"""
        # If name is being updated, check it doesn't conflict
        if vehicle_type_update.name:
            existing = self.repository.get_by_name(vehicle_type_update.name)
            if existing and existing.id != vehicle_type_id:
                raise ValueError(f"Vehicle type with name '{vehicle_type_update.name}' already exists")
        
        updated_vehicle_type = self.repository.update(vehicle_type_id, vehicle_type_update)
        if updated_vehicle_type:
            return VehicleTypeResponse.model_validate(updated_vehicle_type)
        return None

    def delete_vehicle_type(self, vehicle_type_id: int) -> bool:
        """Delete a vehicle type"""
        return self.repository.delete(vehicle_type_id)

    def recommend_vehicle_for_order(
        self, 
        weight_kg: float, 
        volume_m3: Optional[float] = None
    ) -> List[VehicleTypeResponse]:
        """Recommend suitable vehicle types for an order based on weight and volume"""
        suitable_vehicles = self.repository.get_by_capacity(
            min_weight_kg=weight_kg,
            min_volume_m3=volume_m3
        )
        return [VehicleTypeResponse.model_validate(vt) for vt in suitable_vehicles]

    def initialize_default_vehicle_types(self) -> List[VehicleTypeResponse]:
        """Initialize default vehicle types from the dataset"""
        default_vehicles = [
            {
                "name": "1 TONNER",
                "max_weight_kg": 1000,
                "max_volume_m3": 5,
                "average_speed_kmh": 80,
                "cost_per_km": 2.5,
                "is_active": True,
                "description": "Small delivery truck, suitable for light loads"
            },
            {
                "name": "4 TONNER",
                "max_weight_kg": 4000,
                "max_volume_m3": 15,
                "average_speed_kmh": 75,
                "cost_per_km": 4.0,
                "is_active": True,
                "description": "Medium delivery truck, most commonly used"
            },
            {
                "name": "8 TONNER",
                "max_weight_kg": 8000,
                "max_volume_m3": 30,
                "average_speed_kmh": 70,
                "cost_per_km": 6.0,
                "is_active": True,
                "description": "Large delivery truck for heavy loads"
            },
            {
                "name": "12 TONNER",
                "max_weight_kg": 12000,
                "max_volume_m3": 45,
                "average_speed_kmh": 65,
                "cost_per_km": 8.0,
                "is_active": True,
                "description": "Heavy duty truck for very large shipments"
            },
            {
                "name": "15 TONNER",
                "max_weight_kg": 15000,
                "max_volume_m3": 55,
                "average_speed_kmh": 60,
                "cost_per_km": 10.0,
                "is_active": True,
                "description": "Extra heavy duty truck for maximum capacity"
            },
            {
                "name": "20 TONNER",
                "max_weight_kg": 20000,
                "max_volume_m3": 70,
                "average_speed_kmh": 55,
                "cost_per_km": 12.0,
                "is_active": True,
                "description": "Largest truck for exceptional loads"
            }
        ]
        
        created_vehicles = []
        for vehicle_data in default_vehicles:
            # Check if it already exists
            existing = self.repository.get_by_name(vehicle_data["name"])
            if not existing:
                vehicle_create = VehicleTypeCreate(**vehicle_data)
                created_vehicle = self.repository.create(vehicle_create)
                created_vehicles.append(VehicleTypeResponse.model_validate(created_vehicle))
            else:
                created_vehicles.append(VehicleTypeResponse.model_validate(existing))
        
        return created_vehicles
