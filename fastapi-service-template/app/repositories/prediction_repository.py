from sqlalchemy.orm import Session
from typing import Optional, List
import logging
from models.order_prediction import OrderPrediction

logger = logging.getLogger(__name__)


class OrderPredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_id: int, predicted_delay: float, recommended_vehicle_type_id: Optional[int], confidence: Optional[float]) -> OrderPrediction:
        pred = OrderPrediction(
            order_id=order_id,
            predicted_delay_days=float(predicted_delay) if predicted_delay is not None else None,
            recommended_vehicle_type_id=recommended_vehicle_type_id,
            confidence=confidence
        )
        self.db.add(pred)
        self.db.commit()
        self.db.refresh(pred)
        logger.info(f"Saved prediction for order {order_id}: {pred}")
        return pred

    def get_latest_for_order(self, order_id: int) -> Optional[OrderPrediction]:
        return self.db.query(OrderPrediction).filter(OrderPrediction.order_id == order_id).order_by(OrderPrediction.created_at.desc()).first()

    def get_all_for_order(self, order_id: int) -> List[OrderPrediction]:
        return self.db.query(OrderPrediction).filter(OrderPrediction.order_id == order_id).order_by(OrderPrediction.created_at.desc()).all()
