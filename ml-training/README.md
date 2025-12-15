# ML Training Service

This service trains a CatBoost regression model to predict shipping delays.

## Usage

### Training the Model

To train the model, run:

```bash
docker-compose --profile train up ml-training
```

This will:

1. Load the dataset from `./data/south_africa_all_with_weather_clean.csv`
2. Train a CatBoost model
3. Save the trained model to `./models/catboost_model.json`
4. Save model metadata to `./models/model_metadata.json`

### Requirements

- Place your training data CSV file at `./data/south_africa_all_with_weather_clean.csv`
- The CSV should contain the required features and target column (`delay_diff_days`)

### Output

After training, you'll find:

- `./models/catboost_model.json` - The trained CatBoost model in JSON format
- `./models/model_metadata.json` - Model performance metrics and configuration

### Model Features

The model uses the following features:

- **Categorical**: origin_country, origin_city, destination_country, destination_city, ship_dow, vessel, flight_voyage, weight_uq, volume_uq
- **Numerical**: ship_year, ship_month, ship_week, distance_km, leadtime_expected_days, average_distance_per_day, weight, volume, temperature and precipitation data
