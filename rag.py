from src.document_loader import load_documents
from src.vector_store import add_documents
from src.rag import ask_policy


# ============================================================
# DAY 1 RAG PIPELINE TEST
# ============================================================

print("=" * 60)
print("AIRPORT OPERATIONS AI COPILOT")
print("DAY 1 - RAG PIPELINE")
print("=" * 60)


# ============================================================
# 1. LOAD DOCUMENTS
# ============================================================

print("\n1. LOADING POLICY DOCUMENTS")
print("-" * 40)

documents = load_documents()

print(
    f"\nTotal documents loaded: {len(documents)}"
)


# ============================================================
# 2. BUILD VECTOR DATABASE
# ============================================================

print("\n2. BUILDING VECTOR DATABASE")
print("-" * 40)

add_documents(documents)


# ============================================================
# 3. TEST QUESTIONS
# ============================================================

questions = [

    "What is the maximum surge multiplier allowed at SFO?",

    "Can drivers abandon the airport queue at LAX?",

    "What approval is required before increasing surge at SFO?",

    "What are the pickup restrictions at JFK?",

    "What is the driver cancellation policy at LAX?"
]


# ============================================================
# 4. RUN RAG
# ============================================================

print("\n3. RAG QUESTIONS")
print("=" * 60)


for i, question in enumerate(
    questions,
    start=1
):

    print(f"\nQUESTION {i}")
    print("-" * 40)

    print(question)

    try:

        result = ask_policy(
            question,
            top_k=3
        )

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCE:")
        for source in result["sources"]:
            print(f"- {source}")

        print("\nRETRIEVED CHUNKS:")
        for j, document in enumerate(
            result["retrieved_documents"],
            start=1
        ):

            print(
                f"\nChunk {j}:"
            )

            print(
                document[:300]
            )

    except Exception as e:

        print(
            f"\nERROR: {e}"
        )


print("\n")
print("=" * 60)
print("DAY 1 RAG TEST COMPLETE")
print("=" * 60)