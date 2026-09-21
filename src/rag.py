import os
import time

from dotenv import load_dotenv
from google import genai

from src.vector_store import search_policy


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=api_key
)


# ============================================================
# GEMINI CALL WITH RETRY
# ============================================================

def generate_with_retry(prompt, max_retries=4):

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_text = str(e)

            # Retry only temporary server/rate-limit errors
            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < max_retries - 1:

                    wait_time = 5 * (2 ** attempt)

                    print(
                        f"\nGemini temporarily unavailable."
                    )

                    print(
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    raise e

            else:

                raise e


# ============================================================
# RAG FUNCTION
# ============================================================

def ask_policy(question, top_k=3):

    # --------------------------------------------------------
    # 1. RETRIEVE POLICY CHUNKS
    # --------------------------------------------------------

    results = search_policy(
        question,
        top_k=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]


    # --------------------------------------------------------
    # 2. BUILD CONTEXT
    # --------------------------------------------------------

    context_parts = []
    sources = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        source = metadata["source"]

        context_parts.append(
            f"[Source: {source}]\n{document}"
        )

        if source not in sources:
            sources.append(source)


    context = "\n\n".join(context_parts)


    # --------------------------------------------------------
    # 3. GROUNDED PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are an Airport Operations Policy Assistant.

Answer the user's question using ONLY the supplied
airport policy context.

Rules:
- Do not use outside knowledge.
- Do not invent policy rules.
- If the context does not contain the answer, say:
  "The available policy documents do not contain enough
  information to answer this."
- Give a concise answer.
- Identify the relevant source document.

POLICY CONTEXT:
----------------
{context}
----------------

USER QUESTION:
{question}

Answer using only the policy context.
"""


    # --------------------------------------------------------
    # 4. GENERATE ANSWER
    # --------------------------------------------------------

    answer = generate_with_retry(prompt)


    # --------------------------------------------------------
    # 5. RETURN RESULT
    # --------------------------------------------------------

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_documents": documents
    }