from src.rag.service import RAGService


class FakeRetriever:

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[dict]:

        return [
            {
                "content": "Un retard de 3 à 7 jours nécessite la création d'un ticket.",
                "file_name": "01_delivery_policy.md",
                "source": "documents/01_delivery_policy.md",
                "score": 0.92,
            },
            {
                "content": "Les incidents importants doivent être escaladés.",
                "file_name": "05_escalation_policy.md",
                "source": "documents/05_escalation_policy.md",
                "score": 0.87,
            },
        ]


def test_retrieve_context():

    retriever = FakeRetriever()

    rag_service = RAGService(
        retriever=retriever,
    )

    context = rag_service.retrieve_context(
        "Que faire si une livraison a 5 jours de retard ?"
    )

    assert "01_delivery_policy.md" in context
    assert "05_escalation_policy.md" in context
    assert "3 à 7 jours" in context
    assert "incidents importants" in context


def test_retrieve_context_when_no_results():

    class EmptyRetriever:

        def retrieve(
            self,
            query: str,
            k: int = 5,
        ) -> list[dict]:

            return []

    rag_service = RAGService(
        retriever=EmptyRetriever(),
    )

    context = rag_service.retrieve_context(
        "question inconnue"
    )

    assert context == ""