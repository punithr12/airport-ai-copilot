# ✈️ Airport Operations AI Copilot

An AI-powered **Airport Operations Copilot** that combines **RAG, semantic search, LLM tool calling, operational telemetry, multi-agent reasoning, guardrails, and human-in-the-loop approval** to support airport marketplace and operational decision-making.

The system is designed around the workflow:

    User Query
        ↓
    Understand
        ↓
    Retrieve
        ↓
    Investigate
        ↓
    Reason
        ↓
    Recommend
        ↓
    Validate
        ↓
    Approve
        ↓
    Execute

> **Note:** This project uses synthetic airport policies and synthetic operational telemetry for demonstration and learning purposes. The data does not represent actual airport or Uber operational policies.

---

## 🎯 Project Objective

The goal of this project is to build an end-to-end AI Copilot capable of understanding airport operational questions, retrieving relevant policies, investigating current operational metrics, recommending interventions, validating those recommendations against policy, and executing approved actions.

The system focuses on:

- **SFO** — San Francisco International Airport
- **LAX** — Los Angeles International Airport
- **JFK** — John F. Kennedy International Airport

---

# 🚀 Key Capabilities

## 1. Retrieval-Augmented Generation (RAG)

The Copilot maintains a knowledge base containing synthetic airport policies covering:

- Airport operations
- Pricing and surge policies
- Driver policies
- Operational thresholds
- Approval requirements

### RAG Pipeline

    Policy Documents
          ↓
    Document Loading
          ↓
    Cleaning
          ↓
    Chunking
          ↓
    Embeddings
          ↓
    ChromaDB Vector Store
          ↓
    Semantic Search
          ↓
    Relevant Policy Context
          ↓
    Gemini Response

The system also identifies the policy document used to generate the response.

---

## 2. Synthetic Airport Telemetry

The project contains synthetic operational telemetry for SFO, LAX, and JFK.

The dataset includes:

| Metric | Description |
|---|---|
| `airport_code` | Airport identifier |
| `completion_rate` | Trip completion rate |
| `average_eta` | Average estimated arrival time |
| `active_drivers` | Number of active drivers |
| `driver_cancellation_rate` | Driver cancellation rate |
| `queue_size` | Airport queue size |
| `surge_multiplier` | Current surge multiplier |
| `request_volume` | Number of requests |
| `timestamp` | Metric timestamp |

---

# 🛠️ Operational Tools

The Copilot exposes operational tools that allow the LLM to interact with airport telemetry and perform controlled actions.

## `get_airport_metrics(airport_code)`

Retrieves the latest operational metrics for an airport.

### Example

    User:
    What is happening at SFO?

    AI:
    Calls get_airport_metrics("SFO")

The model uses actual tool output rather than inventing operational metrics.

---

## `calculate_driver_incentive(driver_count, severity_level)`

Calculates a recommended driver incentive and estimated total cost based on the provided driver count and severity level.

### Example

    Driver Count: 100
    Severity: high

    Recommended Incentive: ₹150
    Estimated Total Cost: ₹15,000

> The incentive values are implementation assumptions used for the synthetic project.

---

## `trigger_surge_override(airport_code, new_multiplier, reason)`

Provides a mock execution mechanism for changing the surge multiplier.

### Example

    Airport: SFO
    New Multiplier: 1.5x
    Reason: Low completion rate requires surge adjustment

Day 2 uses mock execution. Approval and policy enforcement are handled as part of the later guardrail/HITL workflow.

---

# 🤖 LLM Function Calling

The system uses **Gemini Function Calling** so that the LLM can determine when operational data is required.

### Example

    User
    "What is happening at SFO?"
            ↓
    Gemini
            ↓
    get_airport_metrics("SFO")
            ↓
    Airport Telemetry
            ↓
    Gemini
            ↓
    Operational Explanation

This prevents the model from fabricating real-time operational metrics.

---

# 🧠 Prompt Engineering

The project includes multiple prompt-engineering approaches:

- P.T.C.F. prompting
- Role-based prompting
- Few-shot prompting
- Structured-output prompting

The prompts are designed to keep responses grounded in the available airport policy information and operational data.

---

# 🔍 Semantic Search

Airport policy documents are converted into embeddings using:

    Sentence Transformers
            ↓
    all-MiniLM-L6-v2
            ↓
    384-dimensional embeddings
            ↓
    ChromaDB

Semantic retrieval is used to identify the most relevant policy documents for a user query.

---

# 🏗️ Project Architecture

    ┌──────────────────┐
    │    User Query    │
    └────────┬─────────┘
             ↓
    ┌──────────────────┐
    │   Gemini LLM     │
    └────────┬─────────┘
             ↓
    ┌─────────────────────────────────────┐
    │                                     │
    ↓                                     ↓
    Policy Required?               Metrics Required?
    ↓                                     ↓
    ┌──────────────────┐          ┌──────────────────┐
    │   RAG Pipeline   │          │ Operational Tools│
    │                  │          │                  │
    │    ChromaDB      │          │     Metrics      │
    │    Embeddings    │          │    Incentives    │
    │    Policies      │          │  Surge Override  │
    └────────┬─────────┘          └────────┬─────────┘
             │                             │
             └─────────────┬───────────────┘
                           ↓
                  ┌─────────────────┐
                  │     Reason /    │
                  │    Recommend    │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │   Guardrails &  │
                  │    Validation   │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Human Approval  │
                  │     (HITL)      │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Mock Execution  │
                  └─────────────────┘

---

# 📁 Project Structure

    airport-ai-copilot/
    │
    ├── README.md
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    ├── app.py
    │
    ├── data/
    │   ├── airport_metrics.csv
    │   │
    │   └── airport_policies/
    │       ├── sfo_operations.md
    │       ├── sfo_pricing.md
    │       ├── sfo_driver_policy.md
    │       ├── lax_operations.md
    │       ├── lax_pricing.md
    │       ├── lax_driver_policy.md
    │       ├── jfk_operations.md
    │       ├── jfk_pricing.md
    │       └── jfk_driver_policy.md
    │
    ├── notebooks/
    │   ├── day1_rag_pipeline.ipynb
    │   ├── day2_tools.ipynb
    │   ├── day3_agents.ipynb
    │   └── day4_guardrails.ipynb
    │
    ├── src/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── document_loader.py
    │   ├── vector_store.py
    │   ├── tools.py
    │   ├── agents.py
    │   ├── agent_day3.py
    │   ├── memory.py
    │   ├── guardrails.py
    │   └── prompts.py
    │
    ├── output/
    │   └── distilled_training_data.jsonl
    │
    └── tests/
        ├── test_rag.py
        ├── test_tools.py
        └── test_guardrails.py

---

# 🔧 Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| LLM | Google Gemini |
| RAG | Retrieval-Augmented Generation |
| Embeddings | Sentence Transformers |
| Embedding Model | `all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| Data Processing | Pandas |
| Prompt Engineering | P.T.C.F., Role-based, Few-shot, Structured Output |
| Tool Calling | Gemini Function Calling |
| UI | Streamlit |
| Version Control | Git & GitHub |

---

# ⚙️ Installation

## 1. Clone the Repository

    git clone https://github.com/punithr12/airport-ai-copilot.git
    cd airport-ai-copilot

---

## 2. Create a Virtual Environment

    python -m venv venv

### Linux / macOS

    source venv/bin/activate

### Windows

    venv\Scripts\activate

---

## 3. Install Dependencies

    pip install -r requirements.txt

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

    GEMINI_API_KEY=your_api_key_here

> **Important:** Never commit the `.env` file to GitHub.

The project includes `.env.example` as a reference for the required environment variables.

---

# ▶️ Running the Project

## Run the RAG Pipeline

    python src/rag.py

---

## Run Operational Tools

    python src/tools.py

---

## Run the Streamlit Application

    streamlit run app.py

---

# 🧪 Example Queries

## Policy Query

    What is the maximum surge allowed at SFO?

The RAG pipeline retrieves the relevant SFO pricing policy and generates a grounded response.

---

## Operational Query

    What is happening at SFO?

The LLM identifies that operational telemetry is required and calls:

    get_airport_metrics("SFO")

The retrieved telemetry is then used to generate an operational explanation.

---

## Intervention Query

    SFO completion rate is low. Can we increase surge to 1.5x?

The complete workflow can combine:

    Operational Metrics
            ↓
    Policy Retrieval
            ↓
    Investigation
            ↓
    Recommendation
            ↓
    Risk Validation
            ↓
    Human Approval
            ↓
    Execution

---

# 🔐 Safety & Guardrails

The project is designed to prevent unsafe or unauthorized operational actions.

The guardrail layer includes:

- Input validation
- Airport validation
- Surge multiplier validation
- Driver count validation
- Severity validation
- Policy validation
- Risk classification
- Human-in-the-loop approval
- Audit trail
- Controlled execution

High-impact operational actions require human approval before execution.

---

# 👤 Human-in-the-Loop

The Copilot does not autonomously execute high-impact operational changes.

The intended flow is:

    AI Recommendation
           ↓
    Risk Assessment
           ↓
    Policy Validation
           ↓
    Human Approval
           ↓
    Execution

This allows the AI to assist with investigation and recommendation while keeping consequential actions under human control.

---

# 🧠 Multi-Agent Reasoning

The project explores multi-agent and ReAct-style reasoning for operational decision-making.

The workflow can be represented as:

    User Request
          ↓
    Investigation
          ↓
    Policy Retrieval
          ↓
    Operational Analysis
          ↓
    Recommendation
          ↓
    Validation
          ↓
    Approval
          ↓
    Execution

The project includes separate modules and notebooks for exploring agent-based workflows.

---

# 💾 Short-Term Memory

The Copilot includes a memory component to maintain relevant information during the reasoning workflow.

Memory can help preserve context between different stages of an operational investigation.

### Example

    User:
    Investigate SFO.

            ↓

    Copilot:
    Retrieves SFO metrics.

            ↓

    User:
    Can we increase surge?

            ↓

    Copilot:
    Uses the previous SFO context while evaluating the request.

---

# 🧪 Testing

The project contains tests covering major components:

    tests/
    ├── test_rag.py
    ├── test_tools.py
    └── test_guardrails.py

Run the test suite using:

    pytest

---

# 📊 Example End-to-End Scenario

### User Request

    Investigate SFO. Completion rate appears to be low.
    Can we increase surge to 1.5x?

### Step 1 — Retrieve Operational Metrics

The Copilot investigates the current operational telemetry:

    Completion Rate: 71%
    Average ETA: 18 minutes
    Driver Cancellation Rate: 19%
    Queue Size: 180

### Step 2 — Retrieve Relevant Policy

The RAG system retrieves the relevant SFO pricing policy and operational policy documents.

### Step 3 — Investigate

The system evaluates the operational situation using the retrieved telemetry and policy information.

### Step 4 — Recommend

The Copilot generates a recommendation based on:

- Current operational conditions
- Relevant policies
- Proposed intervention
- Risk considerations

### Step 5 — Validate

The guardrail layer validates the proposed action against the configured rules and policies.

### Step 6 — Human Approval

High-impact actions are routed for human approval.

### Step 7 — Execute

After approval, the mock execution mechanism can perform the simulated operational action.

---

# 📈 Project Outcomes

This project demonstrates an end-to-end Generative AI workflow combining:

- RAG
- Embeddings
- Vector search
- Prompt engineering
- LLM tool calling
- Operational analytics
- Multi-agent reasoning
- ReAct-style reasoning
- Short-term memory
- Guardrails
- Human-in-the-loop approval
- Auditability
- Synthetic data generation
- Streamlit-based interaction

The project demonstrates how an LLM can move beyond simple question answering and interact with structured data, retrieve organizational knowledge, reason about operational situations, and propose controlled actions.

---

# 📌 Learning Outcomes

Through this project, the following concepts are demonstrated:

- Building a complete RAG pipeline
- Document ingestion and preprocessing
- Text chunking
- Embedding generation
- Vector database implementation
- Semantic search
- LLM prompt engineering
- Gemini function calling
- Tool-based reasoning
- Operational data analysis
- Agent-based workflows
- ReAct-style reasoning
- Short-term conversational memory
- AI guardrails
- Risk validation
- Human-in-the-loop architecture
- Controlled execution
- Synthetic data generation
- Streamlit application development
- Automated testing
- Git and GitHub project management

---

# 🔄 End-to-End AI Copilot Flow

The overall system can be summarized as:

    ┌──────────────────────┐
    │      User Query      │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │    Query Analysis    │
    └──────────┬───────────┘
               ↓
       ┌───────┴────────┐
       ↓                ↓
    Policy           Operational
    Required?         Data Required?
       ↓                ↓
    ┌───────┐       ┌──────────────┐
    │  RAG  │       │ Operational  │
    │Search │       │    Tools     │
    └───┬───┘       └──────┬───────┘
        │                  │
        └────────┬─────────┘
                 ↓
       ┌──────────────────┐
       │    AI Reasoning  │
       └────────┬─────────┘
                ↓
       ┌──────────────────┐
       │   Recommendation │
       └────────┬─────────┘
                ↓
       ┌──────────────────┐
       │   Risk Analysis  │
       └────────┬─────────┘
                ↓
       ┌──────────────────┐
       │ Policy Validation│
       └────────┬─────────┘
                ↓
       ┌──────────────────┐
       │ Human Approval   │
       └────────┬─────────┘
                ↓
       ┌──────────────────┐
       │ Controlled       │
       │ Execution        │
       └──────────────────┘

---

# ⚠️ Disclaimer

This project is an **educational and demonstration system** built using **synthetic airport policies and synthetic operational telemetry**.

The policies, thresholds, metrics, incentive assumptions, and operational actions should **not** be interpreted as actual policies or procedures of:

- SFO
- LAX
- JFK
- Uber
- Any airport authority

The project is intended solely for:

- Learning
- Experimentation
- Generative AI development
- RAG experimentation
- AI-agent architecture demonstrations

---

# 👨‍💻 Author

**Punith R**

AI/ML Engineer | Data Analyst | Generative AI

### GitHub

https://github.com/punithr12

### Project Repository

https://github.com/punithr12/airport-ai-copilot

---

# ⭐ Project Highlights

    RAG
       +
    Semantic Search
       +
    Gemini Function Calling
       +
    Operational Telemetry
       +
    Multi-Agent Reasoning
       +
    Guardrails
       +
    Human-in-the-Loop
       +
    Controlled Execution
       =
    Airport Operations AI Copilot

---

## ⭐ If You Find This Project Useful

If you find this project useful for learning **Generative AI, RAG, LLM Tool Calling, AI Agents, or AI Guardrails**, consider giving the repository a ⭐ on GitHub.