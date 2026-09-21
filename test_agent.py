from src.agents import ask_operations


print("=" * 60)
print("DAY 2 - GEMINI FUNCTION CALLING TEST")
print("=" * 60)


# ============================================================
# TEST 1 — OPERATIONAL QUERY
# ============================================================

print("\nTEST 1")
print("-" * 40)

question = "What's happening at SFO?"

print(f"USER: {question}")

result = ask_operations(question)

print("\nFINAL ANSWER:")
print(result["answer"])


# ============================================================
# TEST 2 — INCENTIVE QUERY
# ============================================================

print("\nTEST 2")
print("-" * 40)

question = (
    "We need incentives for 100 drivers "
    "during a high severity situation."
)

print(f"USER: {question}")

result = ask_operations(question)

print("\nFINAL ANSWER:")
print(result["answer"])


print("\n" + "=" * 60)
print("FUNCTION CALLING TEST COMPLETE")
print("=" * 60)