from src.llm.prompts import PromptBuilder


def test_build_rag_prompt():

    question = "Que faire si une livraison a 5 jours de retard ?"

    context = (
        "Un retard de 3 à 7 jours nécessite "
        "la création d'un ticket."
    )

    prompt = PromptBuilder.build_rag_prompt(
        question=question,
        context=context,
    )

    assert question in prompt
    assert context in prompt
    assert "Ne fabrique jamais d'information" in prompt