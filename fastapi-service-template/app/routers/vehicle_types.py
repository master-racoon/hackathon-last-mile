from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import get_db
from schemas.vehicle_type import VehicleTypeCreate, VehicleTypeResponse
from repositories.vehicle_type_repository import VehicleTypeRepository

router = APIRouter(
    prefix="/vehicle-types",
    tags=["vehicle-types"]
)


@router.get("/", response_model=List[VehicleTypeResponse])
async def get_all_vehicle_types(db: Session = Depends(get_db)):
    """Get all vehicle types"""
    repo = VehicleTypeRepository(db)
    vehicle_types = repo.get_all()
    return vehicle_types


@router.get("/{vehicle_type_id}", response_model=VehicleTypeResponse)
async def get_vehicle_type(vehicle_type_id: int, db: Session = Depends(get_db)):
    """Get a specific vehicle type by ID"""
    repo = VehicleTypeRepository(db)
    vehicle_type = repo.get_by_id(vehicle_type_id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return vehicle_type


@router.post("/", response_model=VehicleTypeResponse, status_code=201)
async def create_vehicle_type(
    vehicle_type: VehicleTypeCreate,
    db: Session = Depends(get_db)
):
    """Create a new vehicle type"""
    repo = VehicleTypeRepository(db)
    
    # Check if vehicle type with same code already exists
    existing = repo.get_by_code(vehicle_type.code)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Vehicle type with code '{vehicle_type.code}' already exists"
        )
    
    return repo.create(vehicle_type)


@router.delete("/{vehicle_type_id}", status_code=204)
async def delete_vehicle_type(vehicle_type_id: int, db: Session = Depends(get_db)):
    """Delete a vehicle type"""
    repo = VehicleTypeRepository(db)
    if not repo.delete(vehicle_type_id):
        raise HTTPException(status_code=404, detail="Vehicle type not found")
