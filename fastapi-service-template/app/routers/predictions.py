from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from predict.predict_open_orders import predict_open_orders

router = APIRouter(
    prefix="/predictions",
    tags=["predictions"]
)


@router.post("/run")
async def run_predictions(db: Session = Depends(get_db)):
    """Trigger a prediction run for open orders. The backend container must have the trained model available at /models/catboost_model.json"""
    try:
        # run prediction synchronously
        predict_open_orders()
        return {"status": "ok", "message": "Prediction run completed"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction run failed: {e}")
