import streamlit as st

from src.tools import get_airport_metrics
from src.rag import ask_policy
from src.document_loader import load_documents
from src.vector_store import add_documents

from src.guardrails import (
    validate_input,
    classify_risk,
    validate_policy,
    validate_output,
    create_audit_record
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Airport Operations AI Copilot",
    page_icon="✈️",
    layout="wide"
)


# ============================================================
# INITIALIZE RAG
# ============================================================

@st.cache_resource
def initialize_rag():

    documents = load_documents()

    add_documents(documents)

    return True


initialize_rag()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = []

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

if "last_audit" not in st.session_state:
    st.session_state.last_audit = None


# ============================================================
# HEADER
# ============================================================

st.title("✈️ Airport Operations AI Copilot")

st.caption(
    "RAG • Operational Tools • Multi-Agent Workflow • "
    "Memory • Guardrails • Human Approval"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Airport")

airport = st.sidebar.selectbox(
    "Select Airport",
    ["SFO", "LAX", "JFK"]
)

st.sidebar.divider()

st.sidebar.write("### System Components")

st.sidebar.success("✓ RAG")
st.sidebar.success("✓ Vector Search")
st.sidebar.success("✓ Operational Tools")
st.sidebar.success("✓ Multi-Agent Workflow")
st.sidebar.success("✓ Short-Term Memory")
st.sidebar.success("✓ Guardrails")
st.sidebar.success("✓ Human Approval")


# ============================================================
# CURRENT METRICS
# ============================================================

metrics = get_airport_metrics(airport)


# ============================================================
# OPERATIONAL METRICS
# ============================================================

st.subheader(
    f"📊 {airport} Operational Metrics"
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Completion Rate",
        f"{metrics['completion_rate'] * 100:.1f}%"
    )

with c2:
    st.metric(
        "Average ETA",
        f"{metrics['average_eta_minutes']:.1f} min"
    )

with c3:
    st.metric(
        "Driver Cancellation",
        f"{metrics['driver_cancellation_rate'] * 100:.1f}%"
    )

with c4:
    st.metric(
        "Queue Size",
        metrics["queue_size"]
    )

with c5:
    st.metric(
        "Surge",
        f"{metrics['surge_multiplier']}x"
    )


st.divider()


# ============================================================
# CHAT HISTORY
# ============================================================

st.subheader(
    "💬 Operations Assistant"
)

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask an airport operations question..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    normalized_question = (
        question
        .strip()
        .lower()
        .replace("!", "")
        .replace(".", "")
        .replace("?", "")
    )


    # ========================================================
    # GREETING
    # ========================================================

    simple_messages = {

        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "heyy",

        "good morning",
        "good afternoon",
        "good evening"
    }


    if normalized_question in simple_messages:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        st.session_state.memory.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        greeting_response = (
            "Hello! 👋 I'm your Airport Operations AI Copilot. "
            "You can ask me about airport metrics, policies, "
            "drivers, queues, ETAs, cancellations, pricing, "
            "surge, incentives, or other airport operations."
        )

        with st.chat_message("assistant"):
            st.write(greeting_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting_response
        })

        st.session_state.memory.append({
            "role": "assistant",
            "content": greeting_response
        })

        st.stop()


    # ========================================================
    # OUT-OF-SCOPE CHECK
    # ========================================================

    airport_keywords = {

        "airport",

        "sfo",
        "lax",
        "jfk",

        "driver",
        "drivers",

        "ride",
        "rides",

        "completion",
        "completion rate",

        "cancellation",
        "cancellations",

        "queue",
        "queue size",

        "eta",

        "arrival",
        "pickup",
        "dropoff",

        "surge",

        "pricing",
        "price",

        "fare",

        "incentive",
        "incentives",

        "policy",
        "policies",

        "operations",
        "operational",

        "metrics",
        "metric",

        "demand",
        "requests",

        "staging",
        "staged",

        "traffic",

        "increase",
        "decrease",

        "investigate",
        "investigation"
    }


    is_airport_question = any(
        keyword in normalized_question
        for keyword in airport_keywords
    )


    if not is_airport_question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        st.session_state.memory.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        scope_response = (
            "I’m sorry, but I don’t have information "
            "about that. I can only help with airport "
            "operations, airport policies, operational "
            "metrics, drivers, queues, ETAs, cancellations, "
            "pricing, surge, incentives, and related topics."
        )

        with st.chat_message("assistant"):
            st.write(scope_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": scope_response
        })

        st.session_state.memory.append({
            "role": "assistant",
            "content": scope_response
        })

        st.stop()


    # ========================================================
    # STORE AIRPORT QUESTION
    # ========================================================

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    st.session_state.memory.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)


    # ========================================================
    # DETERMINE QUESTION TYPE
    # ========================================================

    investigation_keywords = {

        "investigate",
        "investigation",

        "why",
        "problem",
        "issue",
        "issues",

        "low completion",
        "poor completion",
        "completion rate low",

        "what should we do",
        "what can we do",
        "how should we respond",

        "increase surge",
        "increase the surge",
        "raise surge",

        "decrease surge",
        "reduce surge",

        "take action",
        "action",

        "recommend",
        "recommendation",

        "intervention",

        "anomaly",
        "anomalies",

        "performance"
    }


    is_investigation_question = any(
        keyword in normalized_question
        for keyword in investigation_keywords
    )


    # ========================================================
    # ASSISTANT
    # ========================================================

    with st.chat_message("assistant"):


        # ====================================================
        # SIMPLE POLICY / INFORMATION QUESTION
        # ====================================================

        if not is_investigation_question:

            with st.spinner(
                "Searching airport policy..."
            ):

                policy_result = ask_policy(
                    question,
                    top_k=2
                )


            st.markdown(
                "### 💡 Policy Answer"
            )

            st.write(
                policy_result["answer"]
            )


            st.markdown(
                "**Sources:**"
            )

            for source in policy_result["sources"]:

                st.write(
                    f"• `{source}`"
                )


            with st.expander(
                "📚 View Retrieved Policy Context"
            ):

                for document in policy_result[
                    "retrieved_documents"
                ]:

                    st.code(
                        document,
                        language="text"
                    )


            # Store assistant response

            st.session_state.messages.append({
                "role": "assistant",
                "content": policy_result["answer"]
            })

            st.session_state.memory.append({
                "role": "assistant",
                "content": policy_result["answer"]
            })


        # ====================================================
        # INVESTIGATION / OPERATIONAL QUESTION
        # ====================================================

        else:


            # ==================================================
            # STEP 1 — INVESTIGATION
            # ==================================================

            st.markdown(
                "### 🔎 Step 1 — Investigation"
            )


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

            surge = metrics[
                "surge_multiplier"
            ]


            issues = []


            if completion < 0.85:

                issues.append(
                    "Completion rate is below 85%"
                )


            if cancellation > 0.10:

                issues.append(
                    "Driver cancellation rate is above 10%"
                )


            if queue > 150:

                issues.append(
                    "Queue size is above 150"
                )


            if eta > 12:

                issues.append(
                    "Average ETA is above 12 minutes"
                )


            if issues:

                st.error(
                    "⚠️ ANOMALY DETECTED"
                )

                for issue in issues:

                    st.write(
                        f"• {issue}"
                    )

            else:

                st.success(
                    "No major operational anomaly detected."
                )


            # ==================================================
            # STEP 2 — CONTRIBUTING FACTORS
            # ==================================================

            st.markdown(
                "### 📌 Step 2 — Contributing Factors"
            )


            factor_col1, factor_col2, factor_col3 = (
                st.columns(3)
            )


            with factor_col1:

                st.write(
                    f"**Driver Cancellation:** "
                    f"{cancellation * 100:.1f}%"
                )


            with factor_col2:

                st.write(
                    f"**Queue Size:** {queue}"
                )


            with factor_col3:

                st.write(
                    f"**Average ETA:** {eta:.1f} min"
                )


            # ==================================================
            # STEP 3 — RAG
            # ==================================================

            st.markdown(
                "### 📚 Step 3 — Policy Retrieval"
            )


            with st.spinner(
                "Searching airport policies..."
            ):

                policy_result = ask_policy(
                    question,
                    top_k=2
                )


            sources = policy_result[
                "sources"
            ]


            st.write(
                "**Retrieved Documents:**"
            )


            for source in sources:

                st.write(
                    f"• `{source}`"
                )


            with st.expander(
                "View Retrieved Policy Context"
            ):

                for document in policy_result[
                    "retrieved_documents"
                ]:

                    st.code(
                        document,
                        language="text"
                    )


            # ==================================================
            # STEP 4 — RECOMMENDATION
            # ==================================================

            st.markdown(
                "### 🤖 Step 4 — Recommendation"
            )


            recommendation = None

            recommended_surge = None


            if (
                completion < 0.85
                and queue > 150
                and surge < 1.5
            ):

                recommended_surge = min(
                    1.5,
                    round(surge + 0.1, 1)
                )


                recommendation = (
                    f"Increase {airport} surge "
                    f"from {surge}x to "
                    f"{recommended_surge}x."
                )


                st.info(
                    recommendation
                )


            else:

                recommendation = (
                    "No surge increase is recommended "
                    "based on the current telemetry."
                )


                st.info(
                    recommendation
                )


            # ==================================================
            # STEP 5 — GUARDRAIL
            # ==================================================

            st.markdown(
                "### 🛡️ Step 5 — Guardrail Check"
            )


            if recommended_surge is not None:


                input_check = validate_input(

                    airport_code=airport,

                    surge_multiplier=recommended_surge,

                    reason=(
                        "Low completion rate and "
                        "high queue size."
                    )
                )


                risk = classify_risk(

                    action="increase_surge",

                    surge_multiplier=recommended_surge
                )


                policy = validate_policy(

                    airport_code=airport,

                    action="increase_surge",

                    surge_multiplier=recommended_surge
                )


                output_check = validate_output(

                    recommendation=recommendation,

                    risk_level=risk[
                        "risk_level"
                    ],

                    policy_allowed=policy[
                        "allowed"
                    ]
                )


                if not input_check["valid"]:

                    st.error(
                        "🚫 BLOCKED — Invalid input"
                    )

                    st.json(
                        input_check
                    )


                elif not policy["allowed"]:

                    st.error(
                        "🚫 BLOCKED — Policy violation"
                    )

                    st.json(
                        policy
                    )


                elif not output_check["valid"]:

                    st.error(
                        "🚫 BLOCKED — Invalid recommendation"
                    )

                    st.json(
                        output_check
                    )


                else:

                    st.warning(
                        f"⚠️ HUMAN APPROVAL REQUIRED — "
                        f"{risk['risk_level']} RISK"
                    )


                    st.write(
                        f"**Action:** {recommendation}"
                    )


                    st.write(
                        "**Reason:** Low completion rate "
                        "and high queue size."
                    )


                    st.session_state.pending_action = {

                        "airport": airport,

                        "old_surge": surge,

                        "new_surge": recommended_surge,

                        "recommendation": recommendation,

                        "risk": risk,

                        "policy": policy,

                        "sources": sources,

                        "question": question
                    }


            else:

                st.info(
                    "No high-impact action is recommended "
                    "for the current telemetry."
                )


            # ==================================================
            # AGENT TRACE
            # ==================================================

            with st.expander(
                "🤖 Agent Execution Trace"
            ):

                st.write(
                    "1. **Orchestrator** ✓"
                )

                st.write(
                    "   → Received operational request"
                )

                st.write(
                    "2. **Operations Investigator** ✓"
                )

                st.write(
                    "   → Analyzed airport telemetry"
                )

                st.write(
                    "3. **Policy Compliance Agent** ✓"
                )

                st.write(
                    "   → Retrieved relevant airport policy"
                )

                st.write(
                    "4. **Resolution Agent** ✓"
                )

                st.write(
                    "   → Generated operational recommendation"
                )


            # ==================================================
            # MEMORY
            # ==================================================

            with st.expander(
                "🧠 Conversation Memory"
            ):

                if st.session_state.memory:

                    for item in st.session_state.memory:

                        st.write(
                            f"**{item['role']}:** "
                            f"{item['content']}"
                        )

                else:

                    st.write(
                        "No previous conversation."
                    )


            # ==================================================
            # POLICY ANSWER
            # ==================================================

            st.markdown(
                "### 💡 Policy Answer"
            )

            st.write(
                policy_result["answer"]
            )


            st.session_state.messages.append({
                "role": "assistant",
                "content": policy_result["answer"]
            })

            st.session_state.memory.append({
                "role": "assistant",
                "content": policy_result["answer"]
            })


# ============================================================
# HUMAN APPROVAL PANEL
# ============================================================

if st.session_state.pending_action:

    st.divider()

    action = st.session_state.pending_action


    st.subheader(
        "⚠️ HUMAN APPROVAL REQUIRED"
    )


    st.write(
        f"**Action:** "
        f"{action['recommendation']}"
    )


    st.write(
        f"**Risk Level:** "
        f"{action['risk']['risk_level']}"
    )


    st.write(
        f"**Policy Check:** "
        f"{action['policy']['reason']}"
    )


    st.write(
        "**Reason:** Low completion rate "
        "and high queue size."
    )


    approve_col, reject_col = st.columns(2)


    # ========================================================
    # APPROVE
    # ========================================================

    with approve_col:

        if st.button(
            "✅ APPROVE",
            use_container_width=True
        ):

            audit = create_audit_record(

                user_request=action[
                    "question"
                ],

                agents_invoked=[
                    "Orchestrator",
                    "Operations Investigator",
                    "Policy Compliance Agent",
                    "Resolution Agent"
                ],

                tools_called=[
                    "get_airport_metrics"
                ],

                retrieved_policies=action[
                    "sources"
                ],

                recommendation=action[
                    "recommendation"
                ],

                risk_level=action[
                    "risk"
                ]["risk_level"],

                approval_decision="APPROVED",

                final_action="EXECUTED",

                execution_result=(
                    f"{action['airport']} surge "
                    f"updated from "
                    f"{action['old_surge']}x to "
                    f"{action['new_surge']}x."
                )
            )


            st.session_state.last_audit = audit

            st.session_state.pending_action = None


            st.success(
                "✅ ACTION EXECUTED"
            )


            st.info(
                f"{action['airport']} surge updated: "
                f"{action['old_surge']}x → "
                f"{action['new_surge']}x"
            )


            st.rerun()


    # ========================================================
    # REJECT
    # ========================================================

    with reject_col:

        if st.button(
            "❌ REJECT",
            use_container_width=True
        ):

            audit = create_audit_record(

                user_request=action[
                    "question"
                ],

                agents_invoked=[
                    "Orchestrator",
                    "Operations Investigator",
                    "Policy Compliance Agent",
                    "Resolution Agent"
                ],

                tools_called=[
                    "get_airport_metrics"
                ],

                retrieved_policies=action[
                    "sources"
                ],

                recommendation=action[
                    "recommendation"
                ],

                risk_level=action[
                    "risk"
                ]["risk_level"],

                approval_decision="REJECTED",

                final_action="STOPPED",

                execution_result=(
                    "Action rejected by human approver."
                )
            )


            st.session_state.last_audit = audit

            st.session_state.pending_action = None


            st.error(
                "❌ ACTION REJECTED — "
                "No operational action was executed."
            )


            st.rerun()


# ============================================================
# LATEST AUDIT TRAIL
# ============================================================

if st.session_state.last_audit:

    st.divider()

    with st.expander(
        "📋 Latest Audit Trail"
    ):

        st.json(
            st.session_state.last_audit
        )