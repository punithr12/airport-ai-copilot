import chromadb
from sentence_transformers import SentenceTransformer

from document_loader import load_policy_documents, chunk_documents
import os

SYSTEM_CA = "/etc/ssl/certs/ca-certificates.crt"

os.environ["REQUESTS_CA_BUNDLE"] = SYSTEM_CA
os.environ["SSL_CERT_FILE"] = SYSTEM_CA
os.environ["CURL_CA_BUNDLE"] = SYSTEM_CA

print("Using certificate bundle:", SYSTEM_CA)

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "airport_policies"
embedding_model = SentenceTransformer(MODEL_NAME)


def create_embeddings(chunks):
    """Generate embeddings for document chunks."""

    texts = [chunk["content"] for chunk in chunks]

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings


def create_vector_store(chunks, embeddings):
    """Store policy chunks and embeddings in ChromaDB."""

    client = chromadb.PersistentClient(
        path="data/vector_store"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    ids = [f"policy_chunk_{i}" for i in range(len(chunks))]

    documents = [chunk["content"] for chunk in chunks]

    metadatas = [
        {"source": chunk["source"]}
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return collection

def search_policy(query, n_results=3):
    """Retrieve the most relevant policy chunks for a query."""


    client = chromadb.PersistentClient(
        path="data/vector_store"
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    query_embedding = embedding_model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):
        retrieved_chunks.append({
            "content": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })

    return retrieved_chunks


if __name__ == "__main__":
    documents = load_policy_documents()
    chunks = chunk_documents(documents)

    embeddings = create_embeddings(chunks)

    collection = create_vector_store(
        chunks,
        embeddings
    )

    print("\nVector store created successfully")
    print(f"Documents stored: {collection.count()}")

    test_questions = [
        "What is the maximum surge allowed at SFO?",
        "Can drivers abandon the airport queue at SFO?",
        "Does increasing surge require approval at SFO?",
        "What is the expected completion rate at LAX?",
        "What is the maximum surge allowed at JFK?"
    ]

    print("\nPolicy Retrieval Tests")
    print("=" * 70)

    for question in test_questions:
        print(f"\nQuestion: {question}")

        results = search_policy(question, n_results=1)

        result = results[0]

        print(f"Retrieved Source: {result['source']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Content: {result['content'][:250]}...")