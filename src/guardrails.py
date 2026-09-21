# src/guardrails.py
import json
from datetime import datetime
from pathlib import Path

VALID_AIRPORTS = {"SFO", "LAX", "JFK"}

MIN_SURGE = 1.0
MAX_SURGE = 1.5

SURGE_APPROVAL_THRESHOLD = 1.3
HIGH_INCENTIVE_THRESHOLD = 15.0


# ============================================================
# 1. INPUT VALIDATION
# ============================================================

def validate_input(
    airport_code=None,
    surge_multiplier=None,
    driver_count=None,
    incentive_amount=None,
    severity_level=None,
    reason=None
):
    errors = []

    if airport_code is not None:
        airport_code = airport_code.upper().strip()

        if airport_code not in VALID_AIRPORTS:
            errors.append(
                f"Invalid airport code: {airport_code}"
            )

    if surge_multiplier is not None:

        if not isinstance(
            surge_multiplier,
            (int, float)
        ):
            errors.append(
                "Surge multiplier must be numeric."
            )

        elif not MIN_SURGE <= surge_multiplier <= MAX_SURGE:
            errors.append(
                "Surge multiplier must be between 1.0 and 1.5."
            )

    if driver_count is not None:

        if not isinstance(driver_count, int):
            errors.append(
                "Driver count must be an integer."
            )

        elif driver_count <= 0:
            errors.append(
                "Driver count must be greater than 0."
            )

    if incentive_amount is not None:

        if incentive_amount < 0:
            errors.append(
                "Incentive amount cannot be negative."
            )

    if severity_level is not None:

        if severity_level.lower() not in {
            "low",
            "medium",
            "high"
        }:
            errors.append(
                "Severity must be low, medium, or high."
            )

    if reason is not None and not reason.strip():
        errors.append(
            "Reason cannot be empty."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


# ============================================================
# 2. RISK CLASSIFICATION
# ============================================================

def classify_risk(
    action,
    surge_multiplier=None,
    incentive_amount=None
):
    action = action.lower().strip()

    # Low-risk actions
    if action in {
        "read_metrics",
        "search_policy"
    }:
        return {
            "risk_level": "LOW",
            "approval_required": False
        }

    # Incentive calculation
    if action == "calculate_incentive":

        if (
            incentive_amount is not None
            and incentive_amount > HIGH_INCENTIVE_THRESHOLD
        ):
            return {
                "risk_level": "HIGH",
                "approval_required": True
            }

        return {
            "risk_level": "MEDIUM",
            "approval_required": False
        }

    # Surge increase
    if action == "increase_surge":

        if surge_multiplier is None:
            return {
                "risk_level": "HIGH",
                "approval_required": True
            }

        if surge_multiplier >= SURGE_APPROVAL_THRESHOLD:
            return {
                "risk_level": "HIGH",
                "approval_required": True
            }

        return {
            "risk_level": "MEDIUM",
            "approval_required": True
        }

    # Unknown actions are treated as high risk
    return {
        "risk_level": "HIGH",
        "approval_required": True
    }


# ============================================================
# 3. POLICY VALIDATION
# ============================================================

def validate_policy(
    airport_code,
    action,
    surge_multiplier=None
):
    airport_code = airport_code.upper().strip()

    if airport_code not in VALID_AIRPORTS:
        return {
            "allowed": False,
            "reason": "Invalid airport code."
        }

    if action == "increase_surge":

        if surge_multiplier is None:
            return {
                "allowed": False,
                "reason": "Surge multiplier is required."
            }

        if surge_multiplier > MAX_SURGE:
            return {
                "allowed": False,
                "reason": (
                    f"{airport_code} maximum permitted surge "
                    f"is {MAX_SURGE}x."
                )
            }

    return {
        "allowed": True,
        "reason": "Action complies with policy."
    }


# ============================================================
# 4. OUTPUT VALIDATION
# ============================================================

def validate_output(
    recommendation,
    risk_level,
    policy_allowed
):
    errors = []

    if not recommendation:
        errors.append(
            "Recommendation cannot be empty."
        )

    if risk_level not in {
        "LOW",
        "MEDIUM",
        "HIGH"
    }:
        errors.append(
            "Invalid risk level."
        )

    if not policy_allowed:
        errors.append(
            "Recommendation violates policy."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
# ============================================================
# 5. HUMAN APPROVAL
# ============================================================

def request_human_approval(
    action,
    airport_code,
    reason,
    risk_level
):
    """
    Human-in-the-loop approval for medium/high-risk actions.
    """

    if risk_level == "LOW":
        return {
            "approval_required": False,
            "approved": True,
            "decision": "AUTO_APPROVED"
        }

    print("\n" + "=" * 60)
    print("HUMAN APPROVAL REQUIRED")
    print("=" * 60)

    print(f"Action   : {action}")
    print(f"Airport  : {airport_code}")
    print(f"Risk     : {risk_level}")
    print(f"Reason   : {reason}")

    decision = input(
        "\nApprove action? (yes/no): "
    ).strip().lower()

    approved = decision in {"yes", "y"}

    return {
        "approval_required": True,
        "approved": approved,
        "decision": (
            "APPROVED"
            if approved
            else "REJECTED"
        )
    }


# ============================================================
# 6. AUDIT TRAIL
# ============================================================

AUDIT_FILE = Path("output/audit_log.jsonl")


def write_audit_log(record):
    """
    Store every important AI decision as JSONL.
    """

    AUDIT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        AUDIT_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(record)
            + "\n"
        )


def create_audit_record(
    user_request,
    agents_invoked,
    tools_called,
    retrieved_policies,
    recommendation,
    risk_level,
    approval_decision,
    final_action,
    execution_result
):
    """
    Create the complete decision trail.
    """

    record = {
        "timestamp": datetime.now().isoformat(),

        "user_request": user_request,

        "agents_invoked": agents_invoked,

        "tools_called": tools_called,

        "retrieved_policies": retrieved_policies,

        "recommendation": recommendation,

        "risk_level": risk_level,

        "approval_decision": approval_decision,

        "final_action": final_action,

        "execution_result": execution_result
    }

    write_audit_log(record)

    return record