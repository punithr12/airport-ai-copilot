import pandas as pd
from pathlib import Path


# ============================================================
# LOAD AIRPORT OPERATIONAL DATA
# ============================================================

DATA_PATH = Path("data/airport_metrics.csv")

df = pd.read_csv(DATA_PATH)


# ============================================================
# TOOL 1 — GET AIRPORT METRICS
# ============================================================

def get_airport_metrics(airport_code: str):

    airport_code = airport_code.upper().strip()

    valid_airports = ["SFO", "LAX", "JFK"]

    if airport_code not in valid_airports:
        return {
            "status": "error",
            "message": (
                f"Invalid airport code: {airport_code}. "
                f"Valid codes are: {valid_airports}"
            )
        }

    airport_data = df[
        df["airport_code"] == airport_code
    ]

    if airport_data.empty:
        return {
            "status": "error",
            "message": f"No operational data found for {airport_code}"
        }

    # Get the latest telemetry record
    latest = airport_data.sort_values(
        "timestamp"
    ).iloc[-1]

    return {
        "status": "success",
        "airport_code": airport_code,
        "completion_rate": float(latest["completion_rate"]),
        "average_eta_minutes": float(latest["average_eta"]),
        "active_drivers": int(latest["active_drivers"]),
        "driver_cancellation_rate": float(
            latest["driver_cancellation_rate"]
        ),
        "queue_size": int(latest["queue_size"]),
        "surge_multiplier": float(
            latest["surge_multiplier"]
        ),
        "request_volume": int(
            latest["request_volume"]
        ),
        "timestamp": latest["timestamp"]
    }


# ============================================================
# TOOL 2 — DRIVER INCENTIVE CALCULATOR
# ============================================================

def calculate_driver_incentive(
    driver_count: int,
    severity_level: str
):

    if driver_count <= 0:
        return {
            "status": "error",
            "message": "driver_count must be greater than 0"
        }

    severity_level = severity_level.lower().strip()

    incentive_map = {
        "low": 5,
        "medium": 10,
        "high": 20
    }

    if severity_level not in incentive_map:
        return {
            "status": "error",
            "message": (
                "Invalid severity level. "
                "Use low, medium, or high."
            )
        }

    incentive_per_driver = incentive_map[
        severity_level
    ]

    total_cost = driver_count * incentive_per_driver

    return {
        "status": "success",
        "driver_count": driver_count,
        "severity_level": severity_level,
        "recommended_incentive_per_driver": incentive_per_driver,
        "estimated_total_cost": total_cost
    }


# ============================================================
# TOOL 3 — SURGE OVERRIDE
# ============================================================

def trigger_surge_override(
    airport_code: str,
    new_multiplier: float,
    reason: str
):

    airport_code = airport_code.upper().strip()

    valid_airports = ["SFO", "LAX", "JFK"]

    if airport_code not in valid_airports:
        return {
            "status": "error",
            "message": f"Invalid airport code: {airport_code}"
        }

    if new_multiplier < 1.0 or new_multiplier > 1.5:
        return {
            "status": "error",
            "message": (
                "Surge multiplier must be between "
                "1.0 and 1.5."
            )
        }

    if not reason or not reason.strip():
        return {
            "status": "error",
            "message": "A reason is required."
        }

    # Mock execution for Day 2.
    # Approval and permission controls will be
    # implemented during Day 4.

    return {
        "status": "success",
        "airport_code": airport_code,
        "new_multiplier": new_multiplier,
        "reason": reason,
        "message": (
            f"Surge override successfully triggered "
            f"for {airport_code}."
        )
    }