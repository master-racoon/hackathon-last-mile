# Vehicle Types Feature

This document describes the vehicle types functionality integrated into the Last Mile delivery system.

## Overview

The vehicle types feature allows you to:

- Define different types of delivery vehicles with their specifications
- Assign vehicle types to customer orders
- Confirm orders by selecting an appropriate vehicle type
- Query orders by vehicle type
- Get vehicle recommendations based on order weight and volume

## Data Model

### VehicleType Model

The `VehicleType` model includes the following fields:

- `id`: Primary key
- `name`: Vehicle type name (e.g., "8 TONNER", "12 TONNER")
- `max_weight_kg`: Maximum weight capacity in kilograms
- `max_volume_m3`: Maximum volume capacity in cubic meters
- `length_m`, `width_m`, `height_m`: Physical dimensions in meters
- `average_speed_kmh`: Average speed in km/h
- `fuel_consumption_per_100km`: Fuel consumption per 100km
- `cost_per_km`: Operating cost per kilometer
- `daily_rental_cost`: Daily rental cost
- `is_active`: Whether the vehicle type is currently available
- `description`: Additional notes about the vehicle type

### CustomerOrder Model

The `CustomerOrder` model has been updated to include:

- `vehicle_type_id`: Foreign key to VehicleType (nullable)
- `vehicle_type`: Relationship to VehicleType model

## API Endpoints

### Vehicle Types

#### GET /vehicle-types/

Get all vehicle types with optional filtering:

- Query params: `skip`, `limit`, `active_only`

#### GET /vehicle-types/{vehicle_type_id}

Get a specific vehicle type by ID

#### GET /vehicle-types/by-name/{name}

Get a specific vehicle type by name

#### POST /vehicle-types/

Create a new vehicle type

- Body: `VehicleTypeCreate` schema

#### PUT /vehicle-types/{vehicle_type_id}

Update an existing vehicle type

- Body: `VehicleTypeUpdate` schema

#### DELETE /vehicle-types/{vehicle_type_id}

Delete a vehicle type

#### GET /vehicle-types/recommend/for-order

Get vehicle recommendations based on order requirements

- Query params: `weight_kg` (required), `volume_m3` (optional)

#### POST /vehicle-types/initialize

Initialize default vehicle types from the dataset (one-time setup)

### Customer Orders (Vehicle Type Integration)

#### POST /orders/{order_id}/confirm

Confirm a customer order by assigning a vehicle type

- Query param: `vehicle_type_id`
- Updates order status to "confirmed"

#### GET /orders/by-vehicle-type/{vehicle_type_id}

Get all orders assigned to a specific vehicle type

- Query params: `skip`, `limit`

## Default Vehicle Types

The system includes 6 default vehicle types based on the South Africa dataset:

| Name      | Max Weight (kg) | Max Volume (m³) | Avg Speed (km/h) | Cost/km |
| --------- | --------------- | --------------- | ---------------- | ------- |
| 1 TONNER  | 1,000           | 5               | 80               | 2.5     |
| 4 TONNER  | 4,000           | 15              | 75               | 4.0     |
| 8 TONNER  | 8,000           | 30              | 70               | 6.0     |
| 12 TONNER | 12,000          | 45              | 65               | 8.0     |
| 15 TONNER | 15,000          | 55              | 60               | 10.0    |
| 20 TONNER | 20,000          | 70              | 55               | 12.0    |

## Usage Examples

### 1. Initialize Default Vehicle Types

```bash
curl -X POST http://localhost:8000/vehicle-types/initialize
```

### 2. Get Vehicle Recommendation

```bash
curl "http://localhost:8000/vehicle-types/recommend/for-order?weight_kg=5000"
```

### 3. Create a Customer Order

```bash
curl -X POST http://localhost:8000/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_number": "ORD-001",
    "customer_name": "Acme Corp",
    "requested_delivery_date": "2025-12-31",
    "gross_weight_kg": 5500,
    "origin_country": "ZA",
    "destination_country": "ZM",
    "status": "pending"
  }'
```

### 4. Confirm Order with Vehicle Type

```bash
# Assuming order_id=1 and vehicle_type_id=3 (8 TONNER)
curl -X POST "http://localhost:8000/orders/1/confirm?vehicle_type_id=3"
```

### 5. Get Orders by Vehicle Type

```bash
curl http://localhost:8000/orders/by-vehicle-type/3
```

## Testing

A test script is provided to verify the integration:

```bash
python test_vehicle_types.py
```

This script will:

1. Initialize default vehicle types
2. Create a test customer order
3. Confirm the order with an appropriate vehicle type
4. Retrieve orders by vehicle type
5. Verify the integration is working correctly

## Database Schema

The vehicle types feature creates the following table:

```sql
CREATE TABLE vehicle_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    max_weight_kg FLOAT,
    max_volume_m3 FLOAT,
    length_m FLOAT,
    width_m FLOAT,
    height_m FLOAT,
    average_speed_kmh FLOAT,
    fuel_consumption_per_100km FLOAT,
    cost_per_km FLOAT,
    daily_rental_cost FLOAT,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    description TEXT
);

-- Updates to customer_orders table
ALTER TABLE customer_orders
    ADD COLUMN vehicle_type_id INTEGER REFERENCES vehicle_types(id);
```

## Integration Points

### 1. Database Models

- `app/models/vehicle_type.py`: VehicleType model
- `app/models/customer_order.py`: Updated to include vehicle_type relationship

### 2. Schemas

- `app/schemas/vehicle_type.py`: Pydantic schemas for API validation
- `app/schemas/customer_order.py`: Updated to include VehicleTypeResponse

### 3. Repositories

- `app/repositories/vehicle_type_repository.py`: Database operations for vehicle types
- `app/repositories/customer_order_repository.py`: Updated with vehicle type methods

### 4. Services

- `app/services/vehicle_type_service.py`: Business logic for vehicle types

### 5. Routers

- `app/routers/vehicle_types.py`: API endpoints for vehicle types
- `app/routers/orders.py`: Updated with vehicle type confirmation endpoints

### 6. Database Initialization

- `app/init_db.py`: Updated to seed vehicle types on database initialization

## Next Steps

Potential enhancements:

1. Add automatic vehicle recommendation during order creation
2. Implement vehicle availability tracking
3. Add route optimization based on vehicle type
4. Integrate vehicle costs into delivery estimates
5. Add vehicle maintenance scheduling
6. Implement multi-vehicle routing for large orders
