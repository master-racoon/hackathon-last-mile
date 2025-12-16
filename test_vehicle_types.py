#!/usr/bin/env python3
"""
Test script to verify vehicle type integration with customer orders.
This script demonstrates:
1. Creating vehicle types
2. Creating customer orders
3. Confirming orders with vehicle types
4. Retrieving orders by vehicle type
"""

import requests
import json
from datetime import date

# API base URL
BASE_URL = "http://localhost:8000"

def test_vehicle_types():
    """Test vehicle type endpoints"""
    print("\n=== Testing Vehicle Types ===")
    
    # Initialize default vehicle types
    print("\n1. Initializing default vehicle types...")
    response = requests.post(f"{BASE_URL}/vehicle-types/initialize")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        vehicle_types = response.json()
        print(f"Created {len(vehicle_types)} vehicle types:")
        for vt in vehicle_types:
            print(f"  - {vt['name']}: max_weight={vt['max_weight_kg']}kg, max_volume={vt['max_volume_m3']}m3")
    
    # Get all vehicle types
    print("\n2. Getting all vehicle types...")
    response = requests.get(f"{BASE_URL}/vehicle-types/")
    print(f"Status: {response.status_code}")
    vehicle_types = response.json()
    print(f"Found {len(vehicle_types)} vehicle types")
    
    # Get vehicle recommendation
    print("\n3. Getting vehicle recommendation for 5000kg load...")
    response = requests.get(f"{BASE_URL}/vehicle-types/recommend/for-order?weight_kg=5000")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        recommended = response.json()
        print(f"Recommended {len(recommended)} vehicle types:")
        for vt in recommended:
            print(f"  - {vt['name']}: max_weight={vt['max_weight_kg']}kg")
    
    return vehicle_types


def test_customer_orders(vehicle_types):
    """Test customer order endpoints with vehicle types"""
    print("\n=== Testing Customer Orders with Vehicle Types ===")
    
    # Create a test order
    print("\n1. Creating a test customer order...")
    order_data = {
        "order_number": "TEST-ORDER-001",
        "customer_name": "Test Customer",
        "requested_delivery_date": str(date(2025, 12, 31)),
        "origin_country": "ZA",
        "origin_state": "JNB",
        "destination_country": "ZM",
        "destination_state": "LUN",
        "gross_weight_kg": 5500,
        "net_weight_kg": 5000,
        "status": "pending",
        "notes": "Test order for vehicle type integration"
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        order = response.json()
        print(f"Created order: {order['order_number']} (ID: {order['id']})")
        order_id = order['id']
    else:
        print(f"Error: {response.text}")
        return
    
    # Confirm the order with a vehicle type (8 TONNER for 5500kg)
    print("\n2. Confirming order with vehicle type...")
    # Find 8 TONNER vehicle type
    vehicle_8t = next((vt for vt in vehicle_types if vt['name'] == '8 TONNER'), None)
    if vehicle_8t:
        print(f"Using vehicle type: {vehicle_8t['name']} (ID: {vehicle_8t['id']})")
        response = requests.post(
            f"{BASE_URL}/orders/{order_id}/confirm",
            params={"vehicle_type_id": vehicle_8t['id']}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            confirmed_order = response.json()
            print(f"Order confirmed!")
            print(f"  - Status: {confirmed_order['status']}")
            print(f"  - Vehicle Type: {confirmed_order['vehicle_type']['name']}")
            print(f"  - Max Weight: {confirmed_order['vehicle_type']['max_weight_kg']}kg")
    
    # Get orders by vehicle type
    print("\n3. Getting all orders for 8 TONNER vehicle...")
    if vehicle_8t:
        response = requests.get(f"{BASE_URL}/orders/by-vehicle-type/{vehicle_8t['id']}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            orders = response.json()
            print(f"Found {len(orders)} orders for {vehicle_8t['name']}:")
            for order in orders:
                print(f"  - {order['order_number']}: {order['gross_weight_kg']}kg, status={order['status']}")
    
    # Get the specific order to verify vehicle type is set
    print("\n4. Getting order details...")
    response = requests.get(f"{BASE_URL}/orders/{order_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        order = response.json()
        print(f"Order {order['order_number']}:")
        print(f"  - Status: {order['status']}")
        print(f"  - Weight: {order['gross_weight_kg']}kg")
        if order.get('vehicle_type'):
            print(f"  - Vehicle: {order['vehicle_type']['name']}")
            print(f"  - Vehicle Capacity: {order['vehicle_type']['max_weight_kg']}kg")


def main():
    """Main test function"""
    print("=" * 60)
    print("Vehicle Type Integration Test")
    print("=" * 60)
    
    try:
        # Test health endpoint
        print("\nChecking API health...")
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print(f"API is not healthy. Status: {response.status_code}")
            return
        print("API is healthy!")
        
        # Run tests
        vehicle_types = test_vehicle_types()
        test_customer_orders(vehicle_types)
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print(f"\nError: Could not connect to API at {BASE_URL}")
        print("Make sure the backend service is running:")
        print("  docker-compose up backend")
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
