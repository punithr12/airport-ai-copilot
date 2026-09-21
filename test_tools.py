from src.tools import (
    get_airport_metrics,
    calculate_driver_incentive,
    trigger_surge_override
)


print("=" * 60)
print("DAY 2 - OPERATIONAL TOOLS TEST")
print("=" * 60)


# ============================================================
# TEST 1 — AIRPORT METRICS
# ============================================================

print("\n1. GET AIRPORT METRICS")
print("-" * 40)

result = get_airport_metrics("SFO")

print(result)


# ============================================================
# TEST 2 — DRIVER INCENTIVE
# ============================================================

print("\n2. DRIVER INCENTIVE CALCULATOR")
print("-" * 40)

result = calculate_driver_incentive(
    driver_count=100,
    severity_level="high"
)

print(result)


# ============================================================
# TEST 3 — SURGE OVERRIDE
# ============================================================

print("\n3. SURGE OVERRIDE")
print("-" * 40)

result = trigger_surge_override(
    airport_code="SFO",
    new_multiplier=1.5,
    reason="High airport demand and large queue"
)

print(result)


# ============================================================
# TEST 4 — ERROR HANDLING
# ============================================================

print("\n4. ERROR HANDLING")
print("-" * 40)

print(
    get_airport_metrics("ABC")
)

print(
    calculate_driver_incentive(
        driver_count=100,
        severity_level="extreme"
    )
)

print(
    trigger_surge_override(
        airport_code="SFO",
        new_multiplier=2.0,
        reason="High demand"
    )
)


print("\n" + "=" * 60)
print("DAY 2 TOOL TEST COMPLETE")
print("=" * 60)