from src.llm.service import FakeLLMService


def test_fake_llm_generate():

    llm = FakeLLMService()

    response = llm.generate_text(
        "Quelle est la politique de livraison ?"
    )

    assert response is not None
    assert "politique de livraison" in response