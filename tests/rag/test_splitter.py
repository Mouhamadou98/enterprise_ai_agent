from langchain_core.documents import Document

from src.rag.splitter import split_documents


def test_split_documents():
    documents = [
        Document(
            page_content="A" * 2000,
            metadata={"source": "test.md"},
        )
    ]

    chunks = split_documents(documents)

    assert len(chunks) > 1


def test_chunks_keep_metadata():
    documents = [
        Document(
            page_content="A" * 2000,
            metadata={
                "source": "test.md",
                "file_name": "test.md",
            },
        )
    ]

    chunks = split_documents(documents)

    for chunk in chunks:
        assert chunk.metadata["source"] == "test.md"
        assert chunk.metadata["file_name"] == "test.md"


def test_chunk_size():
    documents = [
        Document(
            page_content="A" * 2000,
            metadata={"source": "test.md"},
        )
    ]

    chunks = split_documents(
        documents,
        chunk_size=500,
        chunk_overlap=100,
    )

    for chunk in chunks:
        assert len(chunk.page_content) <= 500