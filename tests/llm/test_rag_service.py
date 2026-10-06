from src.llm.rag_service import RAGLLMService


class FakeRAGService:

    def retrieve_context(self, query: str, k: int = 5) -> str:
        return "Un retard de 3 à 7 jours nécessite la création d'un ticket."


class FakeLLMService:

    def generate_text(self, prompt: str) -> str:
        assert "3 à 7 jours" in prompt
        return "Il faut créer un ticket."


def test_rag_llm_answer():

    service = RAGLLMService(
        rag_service=FakeRAGService(),
        llm_service=FakeLLMService(),
    )

    response = service.answer(
        "Que faire si une livraison a 5 jours de retard ?"
    )

    assert response == "Il faut créer un ticket."