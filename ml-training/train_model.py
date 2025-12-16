import importlib.util, subprocess, sys
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

# Ensure catboost is available when running in containerized environments
if importlib.util.find_spec('catboost') is None:
    print('Installing catboost...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'catboost'])
else:
    print('catboost already installed')

from catboost import CatBoostRegressor, Pool

csv_path = '/data/africa_all_with_weather_clean.csv'
models_dir = Path('/models')

print(f'Loading data from {csv_path}...')
df = pd.read_csv(csv_path)

# Parse dates if present
for col in ['actual_ship', 'actual_delivery']:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

TARGET = 'actual_transit_days'
df = df[df[TARGET].notna()]

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

X = df[feature_cols].copy()
y = pd.to_numeric(df[TARGET], errors='coerce')
mask = y.notna()
X = X[mask]
y = y[mask]

# Impute numerics with median and fill categoricals
for col in num_features:
    if col in X.columns:
        X[col] = pd.to_numeric(X[col], errors='coerce')
        X[col] = X[col].fillna(X[col].median())
for col in cat_features:
    if col in X.columns:
        X[col] = X[col].astype('string').fillna('missing')

cat_indices = [X.columns.get_loc(c) for c in cat_features if c in X.columns]

# Time-based split on ship year
ship_dates = pd.to_datetime(df.loc[y.index, 'actual_ship'], errors='coerce')
train_mask = ship_dates.dt.year < 2025
train_mask = train_mask.fillna(False)

X_train = X[train_mask]
y_train = y[train_mask]
X_test = X[~train_mask]
y_test = y[~train_mask]

print(f'Train rows: {len(X_train)}, Test rows: {len(X_test)}, Cat features: {len(cat_indices)}')

train_pool = Pool(X_train, y_train, cat_features=cat_indices)
test_pool = Pool(X_test, y_test, cat_features=cat_indices)

print('Training main CatBoost duration model...')
model = CatBoostRegressor(
    loss_function='MAE',
    eval_metric='MAE',
    iterations=1000,
    learning_rate=0.05,
    depth=8,
    random_seed=42,
    verbose=200,
    od_type='Iter',
    od_wait=50,
)
model.fit(train_pool, eval_set=test_pool)

preds = model.predict(test_pool)
mae = mean_absolute_error(y_test, preds)
baseline = float(np.median(y_train)) if len(y_train) else 0.0
baseline_mae = mean_absolute_error(y_test, np.full_like(y_test, baseline))
print(f'Duration Test MAE: {mae:.3f} days')
print(f'Baseline (median) MAE: {baseline_mae:.3f} days')

models_dir.mkdir(parents=True, exist_ok=True)

main_model_path = models_dir / 'duration_with_leadtime.json'
model.save_model(main_model_path, format='json')
print(f'Saved main model to {main_model_path}')

medians = {col: float(X[col].median()) for col in num_features if col in X.columns}
meta = {
    'feature_cols': feature_cols,
    'cat_features': [c for c in cat_features if c in X.columns],
    'num_features': [c for c in num_features if c in X.columns],
    'numeric_medians': medians,
    'label': TARGET,
    'test_mae': float(mae),
    'baseline_mae': float(baseline_mae),
    'model_path': main_model_path.name,
}
meta_path = models_dir / 'duration_with_leadtime_meta.json'
meta_path.write_text(json.dumps(meta, indent=2))
print(f'Saved metadata to {meta_path}')

print('Training quantile models for prediction interval...')
q_params = dict(
    iterations=600,
    learning_rate=0.05,
    depth=8,
    random_seed=42,
    verbose=200,
)
q025 = CatBoostRegressor(loss_function='Quantile:alpha=0.025', **q_params)
q975 = CatBoostRegressor(loss_function='Quantile:alpha=0.975', **q_params)

q025.fit(train_pool, eval_set=test_pool)
q975.fit(train_pool, eval_set=test_pool)

p025 = q025.predict(test_pool)
p975 = q975.predict(test_pool)
for i in range(min(5, len(preds))):
    print(f'pred={preds[i]:.2f} days, p2.5={p025[i]:.2f}, p97.5={p975[i]:.2f}, interval_width={p975[i]-p025[i]:.2f}')

q025_path = models_dir / 'duration_with_leadtime_q025.json'
q975_path = models_dir / 'duration_with_leadtime_q975.json'
q025.save_model(q025_path, format='json')
q975.save_model(q975_path, format='json')
print(f'Saved quantile models to {q025_path} and {q975_path}')

quant_meta = {
    'feature_cols': feature_cols,
    'cat_features': [c for c in cat_features if c in X.columns],
    'num_features': [c for c in num_features if c in X.columns],
    'numeric_medians': medians,
    'label': TARGET,
    'quantiles': {'p2_5': q025_path.name, 'p97_5': q975_path.name},
    'test_mae': float(mae),
}
quant_meta_path = models_dir / 'duration_with_leadtime_quantiles_meta.json'
quant_meta_path.write_text(json.dumps(quant_meta, indent=2))
print(f'Saved quantile metadata to {quant_meta_path}')

print('Training completed successfully.')
