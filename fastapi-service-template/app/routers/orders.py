from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from models import get_db
from schemas.customer_order import CustomerOrderCreate, CustomerOrderUpdate, CustomerOrderResponse
from repositories.customer_order_repository import CustomerOrderRepository
from repositories.prediction_repository import OrderPredictionRepository

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.get("/", response_model=List[CustomerOrderResponse])
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all customer orders with optional filtering by status
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **status**: Filter by order status (pending, confirmed, in_transit, delivered, cancelled)
    """
    repo = CustomerOrderRepository(db)
    pred_repo = OrderPredictionRepository(db)
    
    if status:
        orders = repo.get_by_status(status, skip, limit)
    else:
        orders = repo.get_all(skip, limit)
    
    # Attach latest prediction to each order (monkey-patch attribute for Pydantic from_attributes)
    for o in orders:
        try:
            latest = pred_repo.get_latest_for_order(o.id)
            setattr(o, "last_prediction", latest)
        except Exception:
            setattr(o, "last_prediction", None)

    return orders


@router.get("/{order_id}", response_model=CustomerOrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific customer order by ID"""
    repo = CustomerOrderRepository(db)
    order = repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # attach latest prediction
    pred_repo = OrderPredictionRepository(db)
    setattr(order, "last_prediction", pred_repo.get_latest_for_order(order.id))
    return order


@router.get("/by-order-number/{order_number}", response_model=CustomerOrderResponse)
async def get_order_by_number(order_number: str, db: Session = Depends(get_db)):
    """Get a specific customer order by order number"""
    repo = CustomerOrderRepository(db)
    order = repo.get_by_order_number(order_number)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    pred_repo = OrderPredictionRepository(db)
    setattr(order, "last_prediction", pred_repo.get_latest_for_order(order.id))
    return order





@router.get("/{order_id}/recommendations")
async def get_order_recommendations(order_id: int, db: Session = Depends(get_db)):
    """Get all predictions / recommendations for a specific order"""
    pred_repo = OrderPredictionRepository(db)
    preds = pred_repo.get_all_for_order(order_id)
    return preds


@router.post("/", response_model=CustomerOrderResponse, status_code=201)
async def create_order(
    order: CustomerOrderCreate,
    db: Session = Depends(get_db)
):
    """Create a new customer order"""
    repo = CustomerOrderRepository(db)
    
    # Check if order with same order number already exists
    existing = repo.get_by_order_number(order.order_number)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Order with order number '{order.order_number}' already exists"
        )
    
    return repo.create(order)


@router.put("/{order_id}", response_model=CustomerOrderResponse)
async def update_order(
    order_id: int,
    order: CustomerOrderUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing customer order"""
    repo = CustomerOrderRepository(db)
    updated_order = repo.update(order_id, order)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete a customer order"""
    repo = CustomerOrderRepository(db)
    if not repo.delete(order_id):
        raise HTTPException(status_code=404, detail="Order not found")


@router.post("/{order_id}/confirm", response_model=CustomerOrderResponse)
async def confirm_order(
    order_id: int,
    vehicle_type_id: int,
    db: Session = Depends(get_db)
):
    """
    Confirm a customer order by assigning a vehicle type.
    This updates the order status to 'confirmed' and assigns the specified vehicle.
    
    - **order_id**: The ID of the order to confirm
    - **vehicle_type_id**: The ID of the vehicle type to assign
    """
    from repositories.vehicle_type_repository import VehicleTypeRepository
    
    # Verify vehicle type exists
    vehicle_repo = VehicleTypeRepository(db)
    vehicle_type = vehicle_repo.get_by_id(vehicle_type_id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    
    # Confirm the order
    repo = CustomerOrderRepository(db)
    confirmed_order = repo.confirm_order_with_vehicle(order_id, vehicle_type_id)
    if not confirmed_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Attach latest prediction
    pred_repo = OrderPredictionRepository(db)
    setattr(confirmed_order, "last_prediction", pred_repo.get_latest_for_order(confirmed_order.id))
    
    return confirmed_order


@router.get("/by-vehicle-type/{vehicle_type_id}", response_model=List[CustomerOrderResponse])
async def get_orders_by_vehicle_type(
    vehicle_type_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get all orders assigned to a specific vehicle type
    
    - **vehicle_type_id**: The ID of the vehicle type
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    from repositories.vehicle_type_repository import VehicleTypeRepository
    
    # Verify vehicle type exists
    vehicle_repo = VehicleTypeRepository(db)
    vehicle_type = vehicle_repo.get_by_id(vehicle_type_id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    
    repo = CustomerOrderRepository(db)
    orders = repo.get_by_vehicle_type(vehicle_type_id, skip, limit)
    
    # Attach latest prediction to each order
    pred_repo = OrderPredictionRepository(db)
    for o in orders:
        try:
            latest = pred_repo.get_latest_for_order(o.id)
            setattr(o, "last_prediction", latest)
        except Exception:
            setattr(o, "last_prediction", None)
    
    return orders
