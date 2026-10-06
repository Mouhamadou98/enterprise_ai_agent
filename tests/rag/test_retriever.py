from src.rag.retriever import KnowledgeRetriever


class FakeEmbeddingService:

    def embed_query(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


class FakeElasticsearchClient:

    def knn_search(
        self,
        index_name: str,
        query_vector: list[float],
        k: int,
        num_candidates: int,
    ) -> list[dict]:

        return [
            {
                "content": "Les livraisons ayant un retard de 3 à 7 jours nécessitent la création d'un ticket.",
                "file_name": "01_delivery_policy.md",
                "source": "data/acme_logistics/documents/01_delivery_policy.md",
                "score": 0.92,
            }
        ]
    def keyword_search(self,
        index_name: str, query: str, k: int,) -> list[dict]:

        return [
            {
                "content": "Les livraisons ayant un retard de 3 à 7 jours nécessitent la création d'un ticket.",
                "file_name": "01_delivery_policy.md",
                "source": "data/acme_logistics/documents/01_delivery_policy.md",
                "score": 8.5,
            }
        ]


def test_retrieve():
    embedding_service = FakeEmbeddingService()
    elasticsearch_client = FakeElasticsearchClient()

    retriever = KnowledgeRetriever(
        embedding_service=embedding_service,
        elasticsearch_client=elasticsearch_client,
    )

    results = retriever.retrieve(
        "Que faire si une livraison a 5 jours de retard ?"
    )

    assert len(results) == 1
    assert results[0]["file_name"] == "01_delivery_policy.md"
    assert results[0]["score"] > 0