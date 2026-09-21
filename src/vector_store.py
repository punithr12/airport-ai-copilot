import chromadb
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ============================================================
# 1. CHROMA DATABASE
# ============================================================

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)


# ============================================================
# 2. CREATE FRESH COLLECTION
# ============================================================

try:
    chroma_client.delete_collection(
        name="airport_policies"
    )
except Exception:
    pass


collection = chroma_client.create_collection(
    name="airport_policies"
)


# ============================================================
# 3. TEXT SPLITTER
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


# ============================================================
# 4. TF-IDF VECTORIZER
# ============================================================

vectorizer = TfidfVectorizer(
    stop_words="english"
)


# ============================================================
# 5. ADD DOCUMENTS
# ============================================================

def add_documents(documents):

    all_chunks = []
    all_metadata = []
    all_ids = []

    chunk_id = 0

    # -----------------------------
    # Split documents into chunks
    # -----------------------------

    for doc in documents:

        source = doc["source"]
        text = doc["text"]

        chunks = text_splitter.split_text(text)

        print(
            f"{source} -> {len(chunks)} chunks"
        )

        for chunk in chunks:

            if not chunk.strip():
                continue

            all_chunks.append(chunk)

            all_metadata.append({
                "source": source
            })

            all_ids.append(
                str(chunk_id)
            )

            chunk_id += 1


    # -----------------------------
    # Safety check
    # -----------------------------

    if not all_chunks:

        raise ValueError(
            "No chunks were created."
        )


    # -----------------------------
    # Create TF-IDF vectors
    # -----------------------------

    embeddings = vectorizer.fit_transform(
        all_chunks
    ).toarray()


    print(
        f"\nVector dimensions: {embeddings.shape[1]}"
    )


    # -----------------------------
    # Add to Chroma
    # -----------------------------

    collection.add(
        ids=all_ids,
        documents=all_chunks,
        metadatas=all_metadata,
        embeddings=embeddings.tolist()
    )


    print(
        f"Added {len(all_chunks)} chunks to ChromaDB."
    )


# ============================================================
# 6. SEARCH POLICY
# ============================================================

def search_policy(query, top_k=3):

    # Convert query into the same TF-IDF space
    query_vector = vectorizer.transform(
        [query]
    ).toarray()


    results = collection.query(
        query_embeddings=query_vector.tolist(),
        n_results=top_k
    )


    return results