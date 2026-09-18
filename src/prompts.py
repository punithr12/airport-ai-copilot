"""
Prompt templates for the Airport AI Copilot.

Day 1:
- P.T.C.F. prompting
- Role-based prompting
- Few-shot prompting
- Structured-output prompting
"""


def ptcf_policy_prompt(airport_code: str, policy_type: str) -> str:
    """Create a P.T.C.F. prompt for synthetic airport policy generation."""

    return f"""
PERSONA:
You are an Airport Operations Policy Analyst responsible for creating
synthetic policies for an Airport Operations AI Copilot.

TASK:
Create a synthetic {policy_type} policy for {airport_code}.

CONTEXT:
The Airport AI Copilot investigates operational issues using:
- Completion rate
- Average ETA
- Active drivers
- Driver cancellation rate
- Queue size
- Request volume
- Surge multiplier

The policy should contain clear operational rules, thresholds,
restrictions, and escalation guidance where applicable.

The policy must be synthetic and must not represent actual Uber
or airport policy.

FORMAT:
Return the policy as Markdown with clear headings and sections.
""".strip()


def role_based_policy_prompt(airport_code: str, policy_type: str) -> str:
    """Create a role-based policy prompt."""

    return f"""
You are the Policy & Compliance Analyst for an Airport Operations
AI Copilot.

Your responsibilities are to create and evaluate synthetic
airport policies.

You must:
- Identify policy thresholds clearly.
- Identify restrictions.
- Identify approval requirements.
- Never invent operational metrics.
- Clearly distinguish synthetic assumptions from real-world policies.

Create a synthetic {policy_type} policy for {airport_code}.

Return the result in Markdown.
""".strip()


def few_shot_policy_prompt(airport_code: str, policy_type: str) -> str:
    """Create a few-shot policy-generation prompt."""

    return f"""
You are an Airport Operations Policy Analyst.

Example 1:

Input:
Airport: SFO
Policy Type: Pricing

Output:
Maximum permitted surge: 1.5x
Surge increases must be validated against the policy limit.
A proposed surge above 1.5x is a policy violation.


Example 2:

Input:
Airport: LAX
Policy Type: Pricing

Output:
Maximum permitted surge: 1.8x
Surge increases must be validated against the policy limit.
A proposed surge above 1.8x is a policy violation.


Now generate:

Input:
Airport: {airport_code}
Policy Type: {policy_type}

Return:
- Maximum permitted surge
- Surge increase conditions
- Approval requirements
- Policy violation condition
""".strip()


def structured_policy_prompt(airport_code: str, policy_type: str) -> str:
    """Create a structured-output policy prompt."""

    return f"""
You are an Airport Operations Policy Analyst.

Generate a synthetic {policy_type} policy for {airport_code}.

Return ONLY valid JSON using this structure:

{{
    "airport_code": "{airport_code}",
    "policy_type": "{policy_type}",
    "maximum_surge": 0.0,
    "surge_conditions": [],
    "approval_required": false,
    "violation_condition": ""
}}

Rules:
- Return valid JSON only.
- Do not add Markdown.
- Do not add explanations outside the JSON.
- Use synthetic policy assumptions.
""".strip()
