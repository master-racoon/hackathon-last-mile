from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class EmissionsConfig:
    # Emission factors in kg CO2 per km (examples from the doc)
    emission_factors_kg_per_km: Dict[str, float] = None

    # Weight adjustment:
    # We scale emissions by (1 + weight_kg / weight_scale_kg).
    # Example: weight_scale_kg=1000 => +1.0x per additional 1000kg.
    weight_scale_kg: float = 1000.0

    # Temperature adjustment:
    # Increases CO2 slightly above a baseline temperature:
    # multiplier = 1 + max(0, temp_c - temp_baseline_c) * temp_increase_per_c
    temp_baseline_c: float = 20.0
    temp_increase_per_c: float = 0.005  # 0.5% per °C above baseline

    def __post_init__(self):
        if self.emission_factors_kg_per_km is None:
            object.__setattr__(
                self,
                "emission_factors_kg_per_km",
                {
                    "diesel truck": 0.9,
                    "hybrid truck": 0.45,
                    "ev van": 0.15,
                },
            )


def calculate_co2_kg(
    distance_km: float,
    vehicle_type: str,
    weight_kg: float,
    temperature_c: float,
    config: Optional[EmissionsConfig] = None,
) -> float:
    """
    Estimate CO2 emissions (kg) for a shipment:
      1) base = distance_km * emission_factor(vehicle_type)
      2) weight-adjusted = base * (1 + weight_kg / weight_scale_kg)
      3) temp-adjusted = weight-adjusted * (1 + max(0, temp_c - baseline) * temp_increase_per_c)

    Returns:
      CO2 in kg.
    """
    if config is None:
        config = EmissionsConfig()

    if distance_km < 0:
        raise ValueError("distance_km must be >= 0")
    if weight_kg < 0:
        raise ValueError("weight_kg must be >= 0")

    vt = vehicle_type.strip().lower()
    if vt not in config.emission_factors_kg_per_km:
        valid = ", ".join(sorted(config.emission_factors_kg_per_km.keys()))
        raise ValueError(f"Unknown vehicle_type='{vehicle_type}'. Valid: {valid}")

    ef = config.emission_factors_kg_per_km[vt]  # kg CO2 per km

    # Step 1: base emission per trip
    base = distance_km * ef

    # Step 2: weight adjustment
    weight_multiplier = 1.0 + (weight_kg / config.weight_scale_kg)

    # Step 3: temperature adjustment
    temp_delta = max(0.0, temperature_c - config.temp_baseline_c)
    temp_multiplier = 1.0 + temp_delta * config.temp_increase_per_c

    co2 = base * weight_multiplier * temp_multiplier
    return float(co2)


# Optional helper if you have distance in miles in your dataset
def miles_to_km(miles: float) -> float:
    return miles * 1.609344