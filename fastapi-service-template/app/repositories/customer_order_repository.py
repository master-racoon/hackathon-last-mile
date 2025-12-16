from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from models.customer_order import CustomerOrder
from schemas.customer_order import CustomerOrderCreate, CustomerOrderUpdate

logger = logging.getLogger(__name__)


class CustomerOrderRepository:
    """Repository for customer order database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[CustomerOrder]:
        """Get all customer orders with pagination"""
        return self.db.query(CustomerOrder).offset(skip).limit(limit).all()
    
    def get_by_id(self, order_id: int) -> Optional[CustomerOrder]:
        """Get a customer order by ID"""
        return self.db.query(CustomerOrder).filter(CustomerOrder.id == order_id).first()
    
    def get_by_order_number(self, order_number: str) -> Optional[CustomerOrder]:
        """Get a customer order by order number"""
        return self.db.query(CustomerOrder).filter(CustomerOrder.order_number == order_number).first()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[CustomerOrder]:
        """Get customer orders by status"""
        return self.db.query(CustomerOrder).filter(CustomerOrder.status == status).offset(skip).limit(limit).all()
    
    def create(self, order_data: CustomerOrderCreate) -> CustomerOrder:
        """Create a new customer order"""
        db_order = CustomerOrder(**order_data.model_dump())
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        logger.info(f"Created customer order: {db_order.order_number}")
        return db_order
    
    def update(self, order_id: int, order_data: CustomerOrderUpdate) -> Optional[CustomerOrder]:
        """Update an existing customer order"""
        db_order = self.get_by_id(order_id)
        if db_order:
            update_data = order_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_order, key, value)
            self.db.commit()
            self.db.refresh(db_order)
            logger.info(f"Updated customer order ID: {order_id}")
            return db_order
        return None
    
    def delete(self, order_id: int) -> bool:
        """Delete a customer order"""
        db_order = self.get_by_id(order_id)
        if db_order:
            self.db.delete(db_order)
            self.db.commit()
            logger.info(f"Deleted customer order ID: {order_id}")
            return True
        return False
