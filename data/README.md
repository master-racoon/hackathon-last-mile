# Place your training data here

The ML training service expects a file named `south_africa_all_with_weather_clean.csv` in this directory.

## Required Columns

The CSV file should contain the following columns:

### Target Variable

- `delay_diff_days` - The difference in days between expected and actual delivery

### Date Columns

- `actual_ship` - Actual ship date
- `actual_delivery` - Actual delivery date

### Categorical Features

- `origin_country`
- `origin_city`
- `destination_country`
- `destination_city`
- `ship_dow` - Ship day of week
- `vessel`
- `flight_voyage`
- `weight_uq` - Weight unit qualifier
- `volume_uq` - Volume unit qualifier

### Numerical Features

- `ship_year`
- `ship_month`
- `ship_week`
- `distance_km`
- `leadtime_expected_days`
- `average_distance_per_day`
- `weight`
- `volume`
- `origin_temp_mean` - Origin temperature mean
- `origin_temp_max` - Origin temperature max
- `origin_temp_min` - Origin temperature min
- `origin_precip_mm` - Origin precipitation in mm
- `dest_temp_mean` - Destination temperature mean
- `dest_temp_max` - Destination temperature max
- `dest_temp_min` - Destination temperature min
- `dest_precip_mm` - Destination precipitation in mm

## Usage

Once you place the CSV file here, run:

```bash
docker-compose --profile train up ml-training
```
