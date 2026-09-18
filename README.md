# Airport AI Copilot

An end-to-end Airport Operations AI Copilot using Generative AI,
RAG, embeddings, vector search, tool calling, multi-agent workflows,
memory, guardrails, and human-in-the-loop approval.

## Policy Knowledge Base

The Airport AI Copilot uses a synthetic policy knowledge base covering
SFO, LAX, and JFK airport operations.

### Policy Documents

| Document | Airport | Category |
|---|---|---|
| sfo_operations.md | SFO | Airport Operations |
| sfo_pricing.md | SFO | Pricing & Surge |
| sfo_driver_policy.md | SFO | Driver Policy |
| lax_operations.md | LAX | Airport Operations |
| lax_pricing.md | LAX | Pricing & Surge |
| jfk_operations.md | JFK | Airport Operations |
| jfk_pricing.md | JFK | Pricing & Surge |

### Key Policy Fields

The policy documents contain information related to:

- Airport code
- Policy ID
- Completion rate threshold
- Critical completion rate threshold
- Driver queue rules
- Pickup rules
- Drop-off rules
- Surge multiplier limits
- Surge increase conditions
- Approval requirements
- Policy violations
- Operational investigation metrics
- Driver incentives
- Driver cancellation rules

### Synthetic Policy Assumptions

All policy values in this knowledge base are synthetic assumptions
created specifically for this project.

They do not represent actual Uber or airport policies.

### Important Policy Values

| Airport | Expected Completion Rate | Critical Completion Rate | Maximum Surge |
|---|---:|---:|---:|
| SFO | 85% | 75% | 1.5x |
| LAX | 85% | 75% | 1.8x |
| JFK | 83% | 73% | 1.7x |