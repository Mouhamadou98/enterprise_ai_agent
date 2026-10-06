from src.rag.embeddings import EmbeddingService
from src.rag.elasticsearch_client import ElasticsearchClient


class KnowledgeRetriever:

    def __init__(self, embedding_service: EmbeddingService, elasticsearch_client: ElasticsearchClient, index_name: str = "acme_knowledge"):
        self.embedding_service = embedding_service
        self.elasticsearch_client = elasticsearch_client
        self.index_name = index_name

    def retrieve(self, query: str, k: int = 5) -> list[dict]:

        query_vector = self.embedding_service.embed_query(query)

        vector_results = self.elasticsearch_client.knn_search(
            index_name=self.index_name,
            query_vector=query_vector,
            k=k,
            num_candidates=max(k * 4, 20),
        )

        keyword_results = self.elasticsearch_client.keyword_search(
            index_name=self.index_name,
            query=query,
            k=k,
        )

        return self._rrf_fusion(
            vector_results=vector_results,
            keyword_results=keyword_results,
            k=k,
        )

    @staticmethod
    def _rrf_fusion(vector_results: list[dict], keyword_results: list[dict], k: int = 5, rrf_k: int = 60, vector_weight: float = 0.7, keyword_weight: float = 0.3) -> list[dict]:
        
        scores = {}
        documents = {}

        for rank, result in enumerate(vector_results, start=1):
            key = result["content"]

            scores[key] = scores.get(key, 0.0) + vector_weight / (rrf_k + rank)
            documents[key] = result

        for rank, result in enumerate(keyword_results, start=1):
            key = result["content"]

            scores[key] = scores.get(key, 0.0) + keyword_weight / (rrf_k + rank)
            documents[key] = result

        ranked_documents = sorted(
            documents.items(),
            key=lambda item: scores[item[0]],
            reverse=True,
        )

        results = []

        for content, result in ranked_documents[:k]:
            results.append(
                {
                    **result,
                    "score": scores[content],
                }
            )

        return results