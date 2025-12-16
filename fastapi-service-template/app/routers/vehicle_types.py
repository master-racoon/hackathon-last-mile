from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import get_db
from services.vehicle_type_service import VehicleTypeService
from schemas.vehicle_type import VehicleTypeCreate, VehicleTypeUpdate, VehicleTypeResponse

router = APIRouter(
    prefix="/vehicle-types",
    tags=["vehicle-types"]
)


@router.get("/", response_model=List[VehicleTypeResponse])
def get_vehicle_types(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get all vehicle types.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **active_only**: If true, only return active vehicle types
    """
    service = VehicleTypeService(db)
    return service.get_all_vehicle_types(skip, limit, active_only)


@router.get("/{vehicle_type_id}", response_model=VehicleTypeResponse)
def get_vehicle_type(vehicle_type_id: int, db: Session = Depends(get_db)):
    """Get a specific vehicle type by ID"""
    service = VehicleTypeService(db)
    vehicle_type = service.get_vehicle_type_by_id(vehicle_type_id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return vehicle_type


@router.get("/by-name/{name}", response_model=VehicleTypeResponse)
def get_vehicle_type_by_name(name: str, db: Session = Depends(get_db)):
    """Get a specific vehicle type by name"""
    service = VehicleTypeService(db)
    vehicle_type = service.get_vehicle_type_by_name(name)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail=f"Vehicle type '{name}' not found")
    return vehicle_type


@router.post("/", response_model=VehicleTypeResponse, status_code=201)
def create_vehicle_type(vehicle_type: VehicleTypeCreate, db: Session = Depends(get_db)):
    """Create a new vehicle type"""
    service = VehicleTypeService(db)
    try:
        return service.create_vehicle_type(vehicle_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{vehicle_type_id}", response_model=VehicleTypeResponse)
def update_vehicle_type(
    vehicle_type_id: int,
    vehicle_type_update: VehicleTypeUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing vehicle type"""
    service = VehicleTypeService(db)
    try:
        updated_vehicle_type = service.update_vehicle_type(vehicle_type_id, vehicle_type_update)
        if not updated_vehicle_type:
            raise HTTPException(status_code=404, detail="Vehicle type not found")
        return updated_vehicle_type
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{vehicle_type_id}", status_code=204)
def delete_vehicle_type(vehicle_type_id: int, db: Session = Depends(get_db)):
    """Delete a vehicle type"""
    service = VehicleTypeService(db)
    success = service.delete_vehicle_type(vehicle_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return None


@router.get("/recommend/for-order", response_model=List[VehicleTypeResponse])
def recommend_vehicles(
    weight_kg: float,
    volume_m3: float = None,
    db: Session = Depends(get_db)
):
    """
    Recommend suitable vehicle types for an order.
    
    - **weight_kg**: Required weight capacity in kilograms
    - **volume_m3**: Optional volume capacity in cubic meters
    """
    service = VehicleTypeService(db)
    return service.recommend_vehicle_for_order(weight_kg, volume_m3)


@router.post("/initialize", response_model=List[VehicleTypeResponse])
def initialize_default_vehicle_types(db: Session = Depends(get_db)):
    """
    Initialize default vehicle types based on the dataset.
    This is a one-time setup operation.
    """
    service = VehicleTypeService(db)
    return service.initialize_default_vehicle_types()
