from src.guardrails import (
    validate_input,
    classify_risk,
    validate_policy,
    validate_output,
    request_human_approval,
    create_audit_record
)

print("=" * 70)
print("DAY 4 - SAFETY & GUARDRAILS TEST")
print("=" * 70)


# ============================================================
# TEST 1 — INVALID INPUT
# ============================================================

print("\nTEST 1: INVALID INPUT")
print("-" * 50)

result = validate_input(
    airport_code="ABC",
    surge_multiplier=2.0,
    driver_count=-10
)

print(result)

assert result["valid"] is False

print("PASS")


# ============================================================
# TEST 2 — VALID INPUT
# ============================================================

print("\nTEST 2: VALID INPUT")
print("-" * 50)

result = validate_input(
    airport_code="SFO",
    surge_multiplier=1.5,
    reason="Low completion rate"
)

print(result)

assert result["valid"] is True

print("PASS")


# ============================================================
# TEST 3 — HIGH-RISK CLASSIFICATION
# ============================================================

print("\nTEST 3: HIGH-RISK CLASSIFICATION")
print("-" * 50)

result = classify_risk(
    action="increase_surge",
    surge_multiplier=1.5
)

print(result)

assert result["risk_level"] == "HIGH"
assert result["approval_required"] is True

print("PASS")


# ============================================================
# TEST 4 — POLICY VIOLATION
# ============================================================

print("\nTEST 4: POLICY VIOLATION")
print("-" * 50)

result = validate_policy(
    airport_code="SFO",
    action="increase_surge",
    surge_multiplier=2.0
)

print(result)

assert result["allowed"] is False

print("PASS")


# ============================================================
# TEST 5 — POLICY COMPLIANT ACTION
# ============================================================

print("\nTEST 5: POLICY COMPLIANT ACTION")
print("-" * 50)

result = validate_policy(
    airport_code="SFO",
    action="increase_surge",
    surge_multiplier=1.5
)

print(result)

assert result["allowed"] is True

print("PASS")


# ============================================================
# TEST 6 — OUTPUT VALIDATION
# ============================================================

print("\nTEST 6: OUTPUT VALIDATION")
print("-" * 50)

result = validate_output(
    recommendation="Increase SFO surge to 1.5x",
    risk_level="HIGH",
    policy_allowed=True
)

print(result)

assert result["valid"] is True

print("PASS")


# ============================================================
# TEST 7 — HUMAN APPROVAL
# ============================================================

print("\nTEST 7: HUMAN APPROVAL")
print("-" * 50)

approval = request_human_approval(
    action="Increase SFO surge to 1.5x",
    airport_code="SFO",
    reason="Low completion rate",
    risk_level="HIGH"
)

print(approval)

if approval["approved"]:
    print("Human approved the action.")
else:
    print("Human rejected the action.")


# ============================================================
# TEST 8 — AUDIT TRAIL
# ============================================================

print("\nTEST 8: AUDIT TRAIL")
print("-" * 50)

audit = create_audit_record(
    user_request="Increase SFO surge",
    agents_invoked=[
        "Orchestrator",
        "Operations Investigator",
        "Policy Agent",
        "Resolution Agent"
    ],
    tools_called=[
        "get_airport_metrics"
    ],
    retrieved_policies=[
        "sfo_pricing.md"
    ],
    recommendation="Increase SFO surge to 1.5x",
    risk_level="HIGH",
    approval_decision=approval["decision"],
    final_action=(
        "EXECUTED"
        if approval["approved"]
        else "STOPPED"
    ),
    execution_result=(
        "Action executed successfully."
        if approval["approved"]
        else "Action rejected by human."
    )
)

print(audit)

print("\nPASS")


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("ALL DAY 4 TESTS COMPLETED")
print("=" * 70)