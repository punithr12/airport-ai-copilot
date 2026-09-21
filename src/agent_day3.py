import os
import json

from dotenv import load_dotenv
from google import genai

from src.tools import (
    get_airport_metrics,
    calculate_driver_incentive,
    trigger_surge_override
)

from src.rag import ask_policy
from src.memory import ConversationMemory

from src.document_loader import load_documents
from src.vector_store import add_documents


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )

client = genai.Client(
    api_key=api_key
)


# ============================================================
# INITIALIZE RAG KNOWLEDGE BASE
# ============================================================

print("\nInitializing RAG knowledge base...")

documents = load_documents()

add_documents(documents)

print("RAG knowledge base ready.\n")


# ============================================================
# CONVERSATION MEMORY
# ============================================================

memory = ConversationMemory(
    max_messages=10
)


# ============================================================
# AGENT 1 — OPERATIONS INVESTIGATOR
# ============================================================

def operations_investigator(airport_code):

    print("\n[INVESTIGATOR AGENT]")
    print(
        f"Investigating airport: {airport_code}"
    )

    metrics = get_airport_metrics(
        airport_code
    )

    # Handle tool errors
    if metrics["status"] == "error":

        return metrics

    completion = metrics[
        "completion_rate"
    ]

    eta = metrics[
        "average_eta_minutes"
    ]

    cancellation = metrics[
        "driver_cancellation_rate"
    ]

    queue = metrics[
        "queue_size"
    ]

    issues = []

    # --------------------------------------------------------
    # Identify operational issues
    # --------------------------------------------------------

    if completion < 0.85:

        issues.append(
            "Low completion rate"
        )

    if eta > 12:

        issues.append(
            "High average ETA"
        )

    if cancellation > 0.10:

        issues.append(
            "High driver cancellation rate"
        )

    if queue > 150:

        issues.append(
            "Large airport queue"
        )

    # --------------------------------------------------------
    # Determine severity
    # --------------------------------------------------------

    if not issues:

        severity = "low"

    elif len(issues) >= 3:

        severity = "high"

    else:

        severity = "medium"

    return {
        "airport_code": airport_code,
        "metrics": metrics,
        "issues": issues,
        "severity": severity
    }


# ============================================================
# AGENT 2 — POLICY & COMPLIANCE AGENT
# ============================================================

def policy_compliance_agent(
    question,
    proposed_action
):

    print("\n[POLICY & COMPLIANCE AGENT]")

    print(
        "Searching policy knowledge base..."
    )

    policy_result = ask_policy(
        question,
        top_k=3
    )

    return {
        "proposed_action": proposed_action,

        "policy_answer": (
            policy_result["answer"]
        ),

        "sources": (
            policy_result["sources"]
        ),

        "retrieved_documents": (
            policy_result[
                "retrieved_documents"
            ]
        )
    }


# ============================================================
# AGENT 3 — RESOLUTION AGENT
# ============================================================

def resolution_agent(
    investigation,
    policy_result
):

    print("\n[RESOLUTION AGENT]")

    print(
        "Generating operational recommendation..."
    )

    prompt = f"""
You are the Resolution Agent for an
Airport Operations AI Copilot.

Your job is to analyze the operational
investigation and retrieved policy information
and produce a concise operational recommendation.

OPERATIONAL INVESTIGATION:
{json.dumps(
    investigation,
    indent=2
)}

POLICY & COMPLIANCE INFORMATION:
{json.dumps(
    policy_result,
    indent=2
)}

Provide:

1. Identified operational issue
2. Key contributing factors
3. Recommended actions
4. Policy considerations
5. Whether human approval may be required

Rules:

- Do not invent operational metrics.
- Use only the provided investigation data.
- Use only the provided policy information.
- Keep the recommendation concise.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# ============================================================
# ORCHESTRATOR AGENT
# ============================================================

def orchestrator(
    question,
    airport_code
):

    print("\n" + "=" * 60)
    print("ORCHESTRATOR AGENT")
    print("=" * 60)

    # --------------------------------------------------------
    # Store user message in memory
    # --------------------------------------------------------

    memory.add_message(
        "user",
        question
    )

    # --------------------------------------------------------
    # ReAct iteration control
    # --------------------------------------------------------

    MAX_ITERATIONS = 5

    for iteration in range(
        1,
        MAX_ITERATIONS + 1
    ):

        print(
            f"\nREACT ITERATION {iteration}"
        )

        # ====================================================
        # THINK
        # ====================================================

        print(
            "THINK → Determine required information"
        )

        # ====================================================
        # ACT
        # ====================================================

        print(
            "ACT → Operations Investigator"
        )

        investigation = (
            operations_investigator(
                airport_code
            )
        )

        # ====================================================
        # ERROR CHECK
        # ====================================================

        if investigation.get(
            "status"
        ) == "error":

            return {
                "status": "error",
                "message": investigation[
                    "message"
                ]
            }

        # ====================================================
        # OBSERVE
        # ====================================================

        print(
            "OBSERVE → Investigation completed"
        )

        # ====================================================
        # PROPOSE ACTION
        # ====================================================

        proposed_action = (
            "Consider an operational intervention "
            "based on the current airport conditions."
        )

        # ====================================================
        # ACT → POLICY AGENT
        # ====================================================

        print(
            "ACT → Policy & Compliance Agent"
        )

        policy_result = (
            policy_compliance_agent(
                question,
                proposed_action
            )
        )

        # ====================================================
        # OBSERVE
        # ====================================================

        print(
            "OBSERVE → Policy retrieved"
        )

        # ====================================================
        # ACT → RESOLUTION AGENT
        # ====================================================

        print(
            "ACT → Resolution Agent"
        )

        recommendation = (
            resolution_agent(
                investigation,
                policy_result
            )
        )

        # ====================================================
        # OBSERVE
        # ====================================================

        print(
            "OBSERVE → Recommendation generated"
        )

        # ====================================================
        # STORE RESPONSE IN MEMORY
        # ====================================================

        memory.add_message(
            "assistant",
            recommendation
        )

        # ====================================================
        # RETURN FINAL RESULT
        # ====================================================

        return {
            "status": "success",

            "iteration": iteration,

            "investigation": (
                investigation
            ),

            "policy": (
                policy_result
            ),

            "recommendation": (
                recommendation
            ),

            "memory": (
                memory.get_history()
            )
        }

    # ========================================================
    # MAXIMUM ITERATION ERROR
    # ========================================================

    return {
        "status": "error",

        "message": (
            "Maximum ReAct iterations reached."
        )
    }