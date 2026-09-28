from langchain_core.documents import Document

from src.rag.indexer import KnowledgeIndexer


class FakeEmbeddingService:

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return [
            [0.1] * 384
            for _ in texts
        ]


class FakeElasticsearchClient:

    def __init__(self):
        self.indexed_documents = []

    def bulk_index_documents(
        self,
        index_name: str,
        documents: list[dict],
    ) -> int:

        self.indexed_documents.extend(documents)

        return len(documents)
    
def test_index_documents():
    embedding_service = FakeEmbeddingService()
    elasticsearch_client = FakeElasticsearchClient()

    indexer = KnowledgeIndexer(
        embedding_service=embedding_service,
        elasticsearch_client=elasticsearch_client,
    )

    documents = [
        Document(
            page_content="Une livraison est en retard.",
            metadata={
                "file_name": "delivery.md",
                "source": "data/delivery.md",
            },
        )
    ]

    indexed_count = indexer.index_documents(
        documents=documents,
        index_name="acme_knowledge",
    )

    assert indexed_count > 0
    assert len(elasticsearch_client.indexed_documents) == indexed_count

    indexed_document = elasticsearch_client.indexed_documents[0]

    assert indexed_document["content"] == "Une livraison est en retard."
    assert indexed_document["file_name"] == "delivery.md"
    assert indexed_document["source"] == "data/delivery.md"
    assert len(indexed_document["embedding"]) == 384