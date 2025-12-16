"""
CO2 Emissions Calculation Utilities

Calculates CO2 emissions based on distance, weight, temperature, and vehicle emission factor.
"""


def calculate_co2_emissions(
    distance_km: float,
    weight_kg: float,
    temp_c: float,
    emission_factor_kg_per_km: float
) -> float:
    """
    Calculate CO2 emissions for a trip based on the formula:
    
    Step 1: Base emission per trip
        CO2 = distance × emission_factor
    
    Step 2: Weight adjustment
        CO2_adjusted = CO2 × (1 + 0.1 × weight_kg/100)
        Increases CO2 by 10% for every 100kg of cargo weight
    
    Step 3: Temperature adjustment
        CO2_final = CO2_adjusted × (1 + 0.01 × (temp_C - 25))
        Increases CO2 slightly for higher temperatures (simulating efficiency loss,
        battery cooling, or diesel efficiency loss).
    
    Args:
        distance_km: Distance to travel in kilometers
        weight_kg: Cargo weight in kilograms
        temp_c: Ambient temperature in Celsius
        emission_factor_kg_per_km: Base emission factor in kg CO2 per km
    
    Returns:
        Total CO2 emissions in kg
    """
    # Step 1: Base emission
    co2_base = distance_km * emission_factor_kg_per_km
    
    # Step 2: Weight adjustment
    weight_factor = 1 + (0.1 * weight_kg / 100)
    co2_adjusted = co2_base * weight_factor
    
    # Step 3: Temperature adjustment
    temp_factor = 1 + (0.01 * (temp_c - 25))
    co2_final = co2_adjusted * temp_factor
    
    return co2_final


def get_emission_factor_for_vehicle(vehicle_type) -> float:
    """
    Get the emission factor for a vehicle type.
    
    If emission_factor_kg_per_km is set, use that.
    Otherwise, calculate based on vehicle type:
    - Diesel: ~0.27 kg CO2/km (based on diesel consumption)
    - EV: ~0.05-0.1 kg CO2/km (based on grid carbon intensity)
    - Hybrid: average of diesel and EV
    
    Args:
        vehicle_type: VehicleType model instance
    
    Returns:
        Emission factor in kg CO2 per km
    """
    if vehicle_type.emission_factor_kg_per_km is not None:
        return vehicle_type.emission_factor_kg_per_km
    
    # Fallback calculation based on fuel type
    if vehicle_type.diesel:
        # Diesel: ~2.68 kg CO2 per liter, typical consumption ~10-15 L/100km
        # Using diesel_l_per_km if available
        if vehicle_type.diesel_l_per_km:
            return vehicle_type.diesel_l_per_km * 2.68  # kg CO2 per liter
        return 0.27  # Default for diesel trucks
    
    elif vehicle_type.ev_van:
        # EV: Grid carbon intensity in South Africa ~0.95 kg CO2/kWh
        # Using ev_energy_kwh_per_km if available
        if vehicle_type.ev_energy_kwh_per_km:
            return vehicle_type.ev_energy_kwh_per_km * 0.95  # SA grid carbon intensity
        return 0.08  # Default for EV vans
    
    elif vehicle_type.hybrid:
        # Hybrid: average of diesel and EV
        return 0.175  # (0.27 + 0.08) / 2
    
    # Default fallback
    return 0.20
