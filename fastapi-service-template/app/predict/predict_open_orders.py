"""
Predict open orders using trained CatBoost model and save predictions to the database.
Run this script inside the backend container (backend must have access to /models/catboost_model.json)
"""
import os
import logging
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
    from catboost import CatBoostRegressor, Pool
except Exception as e:
    raise RuntimeError("Required ML packages are not installed in this environment: pandas, numpy, catboost") from e

from models import SessionLocal
from models.customer_order import CustomerOrder
from repositories.prediction_repository import OrderPredictionRepository
from repositories.vehicle_type_repository import VehicleTypeRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = Path("/models/catboost_model.json")

# Features that were used in training (best-effort matching)
CAT_FEATURES = [
    'origin_country', 'origin_city', 'destination_country', 'destination_city',
    'ship_dow', 'vessel', 'flight_voyage', 'weight_uq', 'volume_uq'
]
NUM_FEATURES = [
    'ship_year', 'ship_month', 'ship_week',
    'distance_km', 'leadtime_expected_days', 'average_distance_per_day',
    'weight', 'volume',
    'origin_temp_mean', 'origin_temp_max', 'origin_temp_min', 'origin_precip_mm',
    'dest_temp_mean', 'dest_temp_max', 'dest_temp_min', 'dest_precip_mm'
]
FEATURE_COLS = CAT_FEATURES + NUM_FEATURES


def load_model(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {path}. Train model with the ml-training service first.")
    model = CatBoostRegressor()
    model.load_model(str(path), format='json')
    return model


def build_row_from_order(order: CustomerOrder):
    """Construct a dict of features for a given order. If some features aren't available, leave as NaN/None."""
    row = {}
    # Map available fields - updated to match new model field names
    row['origin_country'] = getattr(order, 'origin_country', None)
    row['origin_city'] = getattr(order, 'origin_state', None)  # Using origin_state as city proxy
    row['destination_country'] = getattr(order, 'destination_country', None)
    row['destination_city'] = getattr(order, 'destination_state', None)  # Using destination_state as city proxy
    
    # ship_dow from load_date if present
    try:
        if order.load_date:
            row['ship_dow'] = order.load_date.weekday()
            row['ship_year'] = order.load_date.year
            row['ship_month'] = order.load_date.month
            row['ship_week'] = order.load_date.isocalendar()[1]
        else:
            row['ship_dow'] = None
            row['ship_year'] = None
            row['ship_month'] = None
            row['ship_week'] = None
    except Exception:
        row['ship_dow'] = None
        row['ship_year'] = None
        row['ship_month'] = None
        row['ship_week'] = None

    # Other numeric-like fields - updated field names
    row['leadtime_expected_days'] = getattr(order, 'lead_time_days', None)
    row['weight'] = getattr(order, 'gross_weight_kg', None)  # Using gross_weight_kg instead of weight_kg
    row['volume'] = None  # volume_m3 not available in new schema

    # placeholders for features not available on order
    for c in FEATURE_COLS:
        if c not in row:
            row[c] = None

    return row


def recommend_vehicle_type(db, weight, volume):
    """Very basic recommendation: choose smallest vehicle type that can fit the weight and volume."""
    vrepo = VehicleTypeRepository(db)
    candidates = vrepo.get_all()
    # Filter out types with no capacity info (keep them but deprioritize)
    fit = []
    for v in candidates:
        fits_weight = (v.max_weight_kg is None) or (weight is None) or (v.max_weight_kg >= weight)
        fits_volume = (v.max_volume_m3 is None) or (volume is None) or (v.max_volume_m3 >= volume)
        if fits_weight and fits_volume:
            fit.append(v)
    if not fit:
        return None
    # choose the one with smallest capacity that still fits (by weight then volume)
    fit_sorted = sorted(fit, key=lambda x: ((x.max_weight_kg or 1e12), (x.max_volume_m3 or 1e12)))
    return fit_sorted[0]


def predict_open_orders():
    logger.info("Starting prediction run for open orders")

    model = load_model(MODEL_PATH)

    db = SessionLocal()
    pred_repo = OrderPredictionRepository(db)

    try:
        # Consider orders with status pending/confirmed/in_transit as "open"
        open_statuses = ['pending', 'confirmed', 'in_transit']
        orders = db.query(CustomerOrder).filter(CustomerOrder.status.in_(open_statuses)).all()

        if not orders:
            logger.info("No open orders found")
            return

        rows = []
        order_map = []
        for o in orders:
            row = build_row_from_order(o)
            rows.append(row)
            order_map.append(o)

        df = pd.DataFrame(rows)

        # Ensure the order of columns matches model expectations (best-effort)
        model_cols = [c for c in FEATURE_COLS if c in df.columns]
        if not model_cols:
            logger.warning("No matching features found between orders and model features. Predictions may be meaningless.")
            model_cols = df.columns.tolist()

        df_for_pred = df[model_cols].copy()
        
        # Fill missing values: convert None to empty string for categorical, 0 for numeric
        for col in df_for_pred.columns:
            if col in CAT_FEATURES:
                df_for_pred[col] = df_for_pred[col].fillna("")
            else:
                df_for_pred[col] = df_for_pred[col].fillna(0)

        cat_cols = [c for c in CAT_FEATURES if c in df_for_pred.columns]
        cat_indices = [df_for_pred.columns.get_loc(c) for c in cat_cols]

        pool = Pool(df_for_pred, cat_features=cat_indices) if cat_indices else Pool(df_for_pred)
        preds = model.predict(pool)

        for o, p in zip(order_map, preds):
            # basic confidence placeholder: not available from plain CatBoost JSON predict
            confidence = None
            # recommend vehicle type - using gross_weight_kg
            rec = recommend_vehicle_type(db, getattr(o, 'gross_weight_kg', None), None)
            rec_id = rec.id if rec else None

            pred_repo.create(order_id=o.id, predicted_delay=float(p), recommended_vehicle_type_id=rec_id, confidence=confidence)

        logger.info(f"Saved predictions for {len(order_map)} orders")

    finally:
        db.close()

if __name__ == '__main__':
    predict_open_orders()
