from src.tools import (
    get_airport_metrics,
    calculate_driver_incentive,
    trigger_surge_override
)

from src.agents import ask_operations


print("=" * 70)
print("AIRPORT OPERATIONS AI COPILOT")
print("DAY 2 - FINAL DEMO")
print("=" * 70)


# ------------------------------------------------------------
# 1. AIRPORT METRICS
# ------------------------------------------------------------

print("\n1. AIRPORT METRICS")
print("-" * 50)

print(get_airport_metrics("SFO"))


# ------------------------------------------------------------
# 2. DRIVER INCENTIVE
# ------------------------------------------------------------

print("\n2. DRIVER INCENTIVE")
print("-" * 50)

print(
    calculate_driver_incentive(
        driver_count=100,
        severity_level="high"
    )
)


# ------------------------------------------------------------
# 3. SURGE OVERRIDE
# ------------------------------------------------------------

print("\n3. SURGE OVERRIDE")
print("-" * 50)

print(
    trigger_surge_override(
        airport_code="SFO",
        new_multiplier=1.5,
        reason="High request volume and large queue"
    )
)


# ------------------------------------------------------------
# 4. GEMINI FUNCTION CALLING
# ------------------------------------------------------------

print("\n4. GEMINI FUNCTION CALLING")
print("-" * 50)

questions = [
    "What's happening at SFO?",
    "How many drivers should receive incentives if severity is high and we need 50 drivers?"
]

for question in questions:

    print(f"\nUSER: {question}")

    result = ask_operations(question)

    print("\nAI:")
    print(result["answer"])


print("\n" + "=" * 70)
print("DAY 2 FINAL DEMO COMPLETE")
print("=" * 70)