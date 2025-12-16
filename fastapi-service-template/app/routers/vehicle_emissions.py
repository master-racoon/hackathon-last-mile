from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import get_db
from schemas.vehicle_emissions import VehicleEmissionsCreate, VehicleEmissionsUpdate, VehicleEmissionsResponse
from repositories.vehicle_emissions_repository import VehicleEmissionsRepository

router = APIRouter(prefix="/vehicle-emissions", tags=["vehicle-emissions"])


@router.get("/", response_model=List[VehicleEmissionsResponse])
def get_all_emissions(db: Session = Depends(get_db)):
    """Get all vehicle emissions records"""
    repo = VehicleEmissionsRepository(db)
    return repo.get_all()


@router.get("/vehicle-type/{vehicle_type_id}", response_model=List[VehicleEmissionsResponse])
def get_emissions_by_vehicle_type(vehicle_type_id: int, db: Session = Depends(get_db)):
    """Get all emission records for a specific vehicle type"""
    repo = VehicleEmissionsRepository(db)
    emissions = repo.get_by_vehicle_type(vehicle_type_id)
    if not emissions:
        raise HTTPException(status_code=404, detail="No emissions data found for this vehicle type")
    return emissions


@router.get("/vehicle-type/{vehicle_type_id}/temperature/{temperature}", response_model=VehicleEmissionsResponse)
def get_emissions_by_temperature(vehicle_type_id: int, temperature: float, db: Session = Depends(get_db)):
    """Get emission record for a specific vehicle type at a given temperature"""
    repo = VehicleEmissionsRepository(db)
    emission = repo.get_by_temperature(vehicle_type_id, temperature)
    if not emission:
        raise HTTPException(
            status_code=404, 
            detail=f"No emissions data found for vehicle type {vehicle_type_id} at temperature {temperature}°C"
        )
    return emission


@router.get("/{emission_id}", response_model=VehicleEmissionsResponse)
def get_emission(emission_id: int, db: Session = Depends(get_db)):
    """Get a specific emission record by ID"""
    repo = VehicleEmissionsRepository(db)
    emission = repo.get_by_id(emission_id)
    if not emission:
        raise HTTPException(status_code=404, detail="Emission record not found")
    return emission


@router.post("/", response_model=VehicleEmissionsResponse, status_code=201)
def create_emission(emission_data: VehicleEmissionsCreate, db: Session = Depends(get_db)):
    """Create a new emission record"""
    repo = VehicleEmissionsRepository(db)
    return repo.create(emission_data)


@router.put("/{emission_id}", response_model=VehicleEmissionsResponse)
def update_emission(emission_id: int, emission_data: VehicleEmissionsUpdate, db: Session = Depends(get_db)):
    """Update an existing emission record"""
    repo = VehicleEmissionsRepository(db)
    emission = repo.update(emission_id, emission_data)
    if not emission:
        raise HTTPException(status_code=404, detail="Emission record not found")
    return emission


@router.delete("/{emission_id}", status_code=204)
def delete_emission(emission_id: int, db: Session = Depends(get_db)):
    """Delete an emission record"""
    repo = VehicleEmissionsRepository(db)
    if not repo.delete(emission_id):
        raise HTTPException(status_code=404, detail="Emission record not found")
    return None
