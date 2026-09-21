from pathlib import Path


def load_documents(data_dir="data/airport_policies"):

    documents = []

    folder = Path(data_dir)

    print(f"Reading from: {folder.resolve()}")
    print()

    for file_path in folder.glob("*.md"):

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        print(
            f"{file_path.name} -> {len(text)} characters"
        )

        if text:

            documents.append({
                "source": file_path.name,
                "text": text
            })

        else:

            print(
                f"WARNING: {file_path.name} is EMPTY"
            )

    print()
    print(
        f"Documents successfully loaded: {len(documents)}"
    )

    return documents