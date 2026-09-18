from pathlib import Path
import re


POLICY_DIR = Path("data/airport_policies")


def clean_text(text):
    """Clean policy document text."""

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def load_policy_documents():
    """
    Load and clean all airport policy Markdown files.

    Returns:
        list[dict]: Each document contains:
            - content
            - source
    """

    documents = []

    for file_path in sorted(POLICY_DIR.glob("*.md")):
        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            continue

        content = clean_text(content)

        documents.append({
            "content": content,
            "source": file_path.name
        })

    return documents


def chunk_documents(documents, chunk_size=500, overlap=100):
    """
    Split documents into overlapping chunks.

    Args:
        documents: Loaded policy documents.
        chunk_size: Maximum characters per chunk.
        overlap: Characters shared between consecutive chunks.

    Returns:
        list[dict]: Chunk content with source metadata.
    """

    chunks = []

    for document in documents:
        text = document["content"]
        source = document["source"]

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append({
                    "content": chunk,
                    "source": source
                })

            if end >= len(text):
                break

            start = end - overlap

    return chunks


if __name__ == "__main__":
    documents = load_policy_documents()
    chunks = chunk_documents(documents)

    print(f"Loaded documents: {len(documents)}")
    print(f"Generated chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks[:5], start=1):
        print(f"Chunk {i}")
        print(f"Source: {chunk['source']}")
        print(f"Characters: {len(chunk['content'])}")
        print("-" * 50)