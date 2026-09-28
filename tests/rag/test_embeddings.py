from src.rag.embeddings import EmbeddingService


def test_embed_documents():
    service = EmbeddingService()

    embeddings = service.embed_documents(
        [
            "Une livraison est en retard.",
            "Une facture doit être payée.",
        ]
    )

    assert len(embeddings) == 2
    assert len(embeddings[0]) > 0
    assert len(embeddings[0]) == len(embeddings[1])


def test_embed_query():
    service = EmbeddingService()

    embedding = service.embed_query(
        "Pourquoi ma livraison est-elle en retard ?"
    )

    assert len(embedding) > 0