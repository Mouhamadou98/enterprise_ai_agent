from src.rag.elasticsearch_client import ElasticsearchClient


def test_elasticsearch_is_available():
    client = ElasticsearchClient()

    assert client.is_available()

def test_create_index():
    client = ElasticsearchClient()

    index_name = "test_acme_knowledge"

    client.create_index(
        index_name=index_name,
        dimensions=384,
    )

    assert client.client.indices.exists(index=index_name)

    client.client.indices.delete(index=index_name)

def test_index_document():
    client = ElasticsearchClient()

    index_name = "test_acme_knowledge"

    client.create_index(
        index_name=index_name,
        dimensions=384,
    )

    embedding = [0.1] * 384

    client.index_document(
        index_name=index_name,
        content="Une livraison est en retard.",
        embedding=embedding,
        metadata={
            "file_name": "test.md",
            "source": "data/test.md",
        },
    )

    client.client.indices.refresh(index=index_name)

    result = client.client.search(
        index=index_name,
        query={
            "match": {
                "content": "livraison",
            }
        },
    )

    assert result["hits"]["total"]["value"] == 1

    hit = result["hits"]["hits"][0]["_source"]

    assert hit["content"] == "Une livraison est en retard."
    assert hit["file_name"] == "test.md"
    assert hit["source"] == "data/test.md"

    client.client.indices.delete(index=index_name)

def test_bulk_index_documents():
    client = ElasticsearchClient()

    index_name = "test_acme_knowledge"

    client.create_index(
        index_name=index_name,
        dimensions=384,
    )

    documents = [
        {
            "content": "Une livraison est en retard.",
            "embedding": [0.1] * 384,
            "file_name": "delivery.md",
            "source": "data/delivery.md",
        },
        {
            "content": "Une facture est impayée.",
            "embedding": [0.2] * 384,
            "file_name": "billing.md",
            "source": "data/billing.md",
        },
    ]

    success = client.bulk_index_documents(
        index_name=index_name,
        documents=documents,
    )

    assert success == 2

    client.client.indices.refresh(index=index_name)

    result = client.client.count(
        index=index_name,
    )

    assert result["count"] == 2

    client.client.indices.delete(index=index_name)