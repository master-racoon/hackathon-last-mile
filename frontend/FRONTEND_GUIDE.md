# LastMile Frontend User Guide

## Overview

The LastMile frontend provides a complete workflow for managing customer orders and viewing ML-powered shipping delay predictions.

## Features

### 1. **View All Customer Orders** (`/`)

The main dashboard shows all customer orders in a table format with:

- Order number
- Customer name
- Status (with color-coded badges)
- Requested delivery date
- **Predicted delay** (from ML model, shown in days)
- Actions (view recommendations)

**Features:**

- **Filter by status**: Click buttons to filter by Pending, Confirmed, In Transit, or Delivered
- **Run Predictions**: Click the "Run Predictions" button to trigger ML model prediction for all open orders
- **Create New Order**: Button to navigate to order creation form

### 2. **Create Customer Order** (`/orders/new`)

A comprehensive form to create a new customer order with all the required fields:

**Basic Information:**

- Order Number (required)
- Customer Name
- Customer Reference
- Confirmation Number

**Dates:**

- Requested Delivery Date (required)
- Load Date
- Estimated Arrival

**Shipping Details:**

- Vehicle Type (dropdown with seeded options)
- Lead Time (days)

**Origin & Destination:**

- Origin City & Country
- Destination City & Country

**Cargo Details:**

- Weight (kg)
- Volume (m³)

**Status & Notes:**

- Status (dropdown: Pending, Confirmed, In Transit, Delivered, Cancelled)
- Additional Notes (textarea)

### 3. **View Recommendations** (`/orders/:orderId/recommendations`)

Shows detailed information about a specific order and its prediction history:

**Order Summary Card:**

- Order details (number, customer, status)
- Requested delivery date
- Load date
- Origin and destination
- Weight and volume

**Prediction History Table:**

- All predictions generated for this order
- Prediction timestamp
- Predicted delay in days (color-coded: red for delays, green for on-time)
- Recommended vehicle type ID
- Confidence score (if available)

## Workflow

### Typical User Flow:

1. **Create Orders**

   - Navigate to "Create New Order"
   - Fill in order details
   - Submit

2. **View Orders**

   - Return to main page
   - See all orders in the table
   - Filter by status if needed

3. **Generate Predictions**

   - Click "Run Predictions" button
   - ML model processes all open orders
   - Predicted delays appear in the table

4. **Review Recommendations**
   - Click "View Recommendations" for any order
   - See full order details and prediction history
   - Use predictions to inform logistics decisions

## API Integration

The frontend communicates with the FastAPI backend at `/backend` (proxied):

- **GET /orders/** - List all orders
- **POST /orders/** - Create new order
- **GET /orders/{id}** - Get single order
- **GET /orders/{id}/recommendations** - Get prediction history
- **POST /predictions/run** - Trigger ML prediction run
- **GET /vehicle-types/** - Get available vehicle types

## Technical Details

- **Framework**: React 18 + TypeScript + Vite
- **UI Components**: Shadcn/ui (built on Radix UI)
- **Styling**: Tailwind CSS
- **Data Fetching**: TanStack Query (React Query)
- **API Client**: Auto-generated from OpenAPI spec using @hey-api/openapi-ts
- **Routing**: React Router v6

## Running the Application

```bash
# Start all services
docker-compose up -d

# Initialize database with vehicle types (first time only)
docker-compose exec backend python init_db.py

# Access the application
# Frontend: http://localhost:3000
# Backend API Docs: http://localhost:8000/docs
```

## Next Steps

1. Train the ML model if not already done:

   ```bash
   docker-compose --profile train up ml-training
   ```

2. Create some test orders through the UI

3. Run predictions to see the ML model in action

4. Review recommendations to make informed shipping decisions
