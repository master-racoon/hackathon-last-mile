from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date, timedelta
import logging
from models.order_prediction import OrderPrediction

logger = logging.getLogger(__name__)


class OrderPredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, 
        order_id: int, 
        expected_lead_time: float,
        predicted_co2: Optional[float] = None,
        recommended_vehicle_type_id: Optional[int] = None,
        destination_track_id: Optional[int] = None,
        confidence: Optional[float] = None,
        requested_arrival_date: Optional[date] = None
    ) -> OrderPrediction:
        """
        Create a new prediction.
        If requested_arrival_date is provided, calculate recommended_booking_date.
        """
        recommended_booking_date = None
        if requested_arrival_date and expected_lead_time:
            # booking_date = requested_arrival - expected_lead_time
            recommended_booking_date = requested_arrival_date - timedelta(days=int(expected_lead_time))
        
        pred = OrderPrediction(
            order_id=order_id,
            expected_lead_time_days=float(expected_lead_time) if expected_lead_time is not None else None,
            predicted_co2_kg=float(predicted_co2) if predicted_co2 is not None else None,
            recommended_vehicle_type_id=recommended_vehicle_type_id,
            destination_track_id=destination_track_id,
            confidence=confidence,
            recommended_booking_date=recommended_booking_date
        )
        self.db.add(pred)
        self.db.commit()
        self.db.refresh(pred)
        logger.info(f"Saved prediction for order {order_id}: lead_time={expected_lead_time}d, booking_date={recommended_booking_date}")
        return pred

    def get_latest_for_order(self, order_id: int) -> Optional[OrderPrediction]:
        return self.db.query(OrderPrediction).filter(OrderPrediction.order_id == order_id).order_by(OrderPrediction.created_at.desc()).first()

    def get_all_for_order(self, order_id: int) -> List[OrderPrediction]:
        return self.db.query(OrderPrediction).filter(OrderPrediction.order_id == order_id).order_by(OrderPrediction.created_at.desc()).all()
