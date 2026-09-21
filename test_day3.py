from src.agents_day3 import orchestrator


print("=" * 70)
print("DAY 3 - MULTI-AGENT AI OPERATIONS COPILOT")
print("=" * 70)


question = (
    "What's happening at SFO and what should "
    "the operations team do?"
)


result = orchestrator(
    question=question,
    airport_code="SFO"
)


print("\n" + "=" * 70)
print("FINAL RESULT")
print("=" * 70)

print("\nSTATUS:")
print(result["status"])

print("\nINVESTIGATION:")
print(result["investigation"])

print("\nPOLICY:")
print(result["policy"])

print("\nRECOMMENDATION:")
print(result["recommendation"])

print("\nMEMORY:")
print(result["memory"])