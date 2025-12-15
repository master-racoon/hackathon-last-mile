import importlib.util, subprocess, sys

pkg = 'catboost'
if importlib.util.find_spec(pkg) is None:
    print('Installing catboost...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'catboost'])
else:
    print('catboost already installed')


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from catboost import CatBoostRegressor, Pool
import json
from pathlib import Path

csv_path = '/data/south_africa_all_with_weather_clean.csv'
output_path = '/models/catboost_model.json'

print(f"Loading data from {csv_path}...")
df = pd.read_csv(csv_path)

# Parse dates if present
for col in ['actual_ship', 'actual_delivery']:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# Target
TARGET = 'delay_diff_days'
df = df[df[TARGET].notna()]

# Feature selection (exclude target and obvious leakage columns)
cat_features = [
    'origin_country', 'origin_city', 'destination_country', 'destination_city',
    'ship_dow', 'vessel', 'flight_voyage', 'weight_uq', 'volume_uq'
]
num_features = [
    'ship_year', 'ship_month', 'ship_week',
    'distance_km', 'leadtime_expected_days', 'average_distance_per_day',
    'weight', 'volume',
    'origin_temp_mean', 'origin_temp_max', 'origin_temp_min', 'origin_precip_mm',
    'dest_temp_mean', 'dest_temp_max', 'dest_temp_min', 'dest_precip_mm'
]
feature_cols = [c for c in cat_features + num_features if c in df.columns]

# Keep only selected columns
X = df[feature_cols].copy()
y = df[TARGET].astype(float)

# Fill missing numeric with median
for col in num_features:
    if col in X.columns:
        X[col] = pd.to_numeric(X[col], errors='coerce')
        X[col] = X[col].fillna(X[col].median())

# Convert categoricals to string and fill missing
for col in cat_features:
    if col in X.columns:
        X[col] = X[col].astype('string').fillna('missing')

# Identify categorical feature indices for CatBoost
cat_indices = [X.columns.get_loc(c) for c in cat_features if c in X.columns]

print(f"Dataset shape: {X.shape}, Target shape: {y.shape}, Categorical features: {len(cat_indices)}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

train_pool = Pool(X_train, y_train, cat_features=cat_indices)
test_pool = Pool(X_test, y_test, cat_features=cat_indices)

print("Training CatBoost model...")
model = CatBoostRegressor(
    loss_function='MAE',
    eval_metric='MAE',
    iterations=600,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    verbose=100,
)
model.fit(train_pool, eval_set=test_pool)

print("\nEvaluating model...")
preds = model.predict(test_pool)
mae = mean_absolute_error(y_test, preds)
print(f"Test MAE: {mae:.3f} days")

# Simple baseline: predict median delay
baseline = np.median(y_train)
baseline_mae = mean_absolute_error(y_test, np.full_like(y_test, baseline))
print(f"Baseline (median) MAE: {baseline_mae:.3f} days")

# Save model in JSON format
print(f"\nSaving model to {output_path}...")
Path(output_path).parent.mkdir(parents=True, exist_ok=True)
model.save_model(output_path, format='json')

# Also save model metadata
metadata = {
    'test_mae': float(mae),
    'baseline_mae': float(baseline_mae),
    'feature_names': list(X.columns),
    'categorical_features': [c for c in cat_features if c in X.columns],
    'numerical_features': [c for c in num_features if c in X.columns],
    'model_params': {
        'iterations': 600,
        'learning_rate': 0.05,
        'depth': 6,
        'loss_function': 'MAE'
    }
}

metadata_path = '/models/model_metadata.json'
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"Model metadata saved to {metadata_path}")
print("Training completed successfully!")
