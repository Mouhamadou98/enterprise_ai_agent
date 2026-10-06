from src.rag.elasticsearch_client import ElasticsearchClient


def main():
    client = ElasticsearchClient()

    query = "delay 3 7 days shipment"

    results = client.keyword_search(
        index_name="acme_knowledge",
        query=query,
        k=5,
    )

    print("\nQuestion :")
    print(query)

    print("\nRésultats BM25 :")

    for i, result in enumerate(results, start=1):
        print(f"\n--- Résultat {i} ---")
        print(f"Score : {result['score']}")
        print(f"Document : {result['file_name']}")
        print(f"Contenu : {result['content']}")


if __name__ == "__main__":
    main()