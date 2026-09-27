from src.rag.loader import DOCUMENTS_DIR, load_directory


def test_load_documents():
    documents = load_directory(DOCUMENTS_DIR)

    assert len(documents) == 10


def test_documents_have_metadata():
    documents = load_directory(DOCUMENTS_DIR)

    for document in documents:
        assert "source" in document.metadata
        assert "file_name" in document.metadata


def test_documents_have_content():
    documents = load_directory(DOCUMENTS_DIR)

    for document in documents:
        assert document.page_content.strip() != ""