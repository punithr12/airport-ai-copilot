import os

from dotenv import load_dotenv
from google import genai

from vector_store import search_policy


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured in .env")

client = genai.Client(api_key=API_KEY)


def generate_rag_response(question, n_results=3):
    """
    Generate a grounded response using retrieved airport policies.
    """

    results = search_policy(
        question,
        n_results=n_results
    )

    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['source']}\n"
            f"Policy Content:\n{result['content']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an Airport Operations AI Copilot.

Answer the user's question using ONLY the policy information
provided in the retrieved context.

Rules:
1. Do not invent policy information.
2. If the retrieved context does not contain enough information,
   clearly say that the policy information is insufficient.
3. Give a concise and factual answer.
4. Identify the source policy document used.
5. Do not use outside knowledge.

Retrieved Policy Context:
{context}

User Question:
{question}

Provide:
- Answer
- Source
"""

    response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

    return response.text, results


if __name__ == "__main__":
    test_questions = [
        "What is the maximum surge allowed at SFO?",
        "Can drivers abandon the airport queue at SFO?",
        "Does increasing surge require approval at SFO?",
        "What is the expected completion rate at LAX?",
        "What is the maximum surge allowed at JFK?"
    ]

    for i, question in enumerate(test_questions, start=1):
        print(f"\n{'=' * 70}")
        print(f"TEST {i}")
        print(f"Question: {question}")
        print("=" * 70)

        answer, results = generate_rag_response(question)

        print("\nRAG RESPONSE:")
        print(answer)

        print("\nSOURCE DOCUMENTS:")
        for result in results:
            print(
                f"- {result['source']} "
                f"(distance={result['distance']:.4f})"
            )
