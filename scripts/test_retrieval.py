from src.rag.embeddings import EmbeddingService
from src.rag.elasticsearch_client import ElasticsearchClient
from src.rag.retriever import KnowledgeRetriever


def main():

    embedding_service = EmbeddingService()

    elasticsearch_client = ElasticsearchClient()

    # retriever = KnowledgeRetriever(
    #     embedding_service=embedding_service,
    #     elasticsearch_client=elasticsearch_client,
    # )

    query = "What happens if a shipment is delayed for 5 days?"
    # query = "Que se passe-t-il si une livraison a 5 jours de retard ?"

    # results = retriever.retrieve(
    #     query=query,
    #     k=5,
    # )

    # print("\nQuestion :")
    # print(query)

    # print("\nRésultats :")

    # for i, result in enumerate(results, start=1):

    #     print(f"\n--- Résultat {i} ---")
    #     print(f"Score : {result['score']}")
    #     print(f"Document : {result['file_name']}")
    #     print(f"Contenu : {result['content']}")

    # query = "Que se passe-t-il si une livraison a 5 jours de retard ?"

    # embedding = embedding_service.embed_query(query)

    # results = elasticsearch_client.knn_search(
    #     index_name="acme_knowledge",
    #     query_vector=embedding,
    #     k=5,
    #     num_candidates=20,
    # )

    # print("\n=== VECTOR SEARCH SEULEMENT ===")

    # for i, result in enumerate(results, start=1):
    #     print(f"\n--- Résultat {i} ---")
    #     print(f"Score : {result['score']}")
    #     print(f"Document : {result['file_name']}")
    #     print(f"Contenu : {result['content']}")

    # query = "Que se passe-t-il si une livraison a 5 jours de retard ?"

    query_vector = embedding_service.embed_query(query)

    vector_results = elasticsearch_client.knn_search(
        index_name="acme_knowledge",
        query_vector=query_vector,
        k=5,
        num_candidates=20,
    )

    keyword_results = elasticsearch_client.keyword_search(
        index_name="acme_knowledge",
        query=query,
        k=5,
    )

    print("\n=== VECTOR SEARCH ===")
    for i, result in enumerate(vector_results, 1):
        print(i, result["file_name"], result["score"])

    print("\n=== BM25 SEARCH ===")
    for i, result in enumerate(keyword_results, 1):
        print(i, result["file_name"], result["score"])

    print("\n=== RRF ===")

    rrf_results = KnowledgeRetriever._rrf_fusion(
        vector_results=vector_results,
        keyword_results=keyword_results,
        k=5,
    )

    for i, result in enumerate(rrf_results, 1):
        print(i, result["file_name"], result["score"])

if __name__ == "__main__":
    main()