from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents, chunk_size=800, chunk_overlap=100):
    """Split loaded documents into overlapping chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )

    chunks = splitter.split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    return chunks


def create_chunks(documents, chunk_size=800, chunk_overlap=100):
    return split_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
