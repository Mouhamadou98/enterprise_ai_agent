from src.llm.factory import LLMFactory


def main():

    llm = LLMFactory.create()

    response = llm.generate_text(
        "Explique en une phrase ce qu'est un système RAG et Agentic RAG."
    )

    print("\nRéponse du LLM :")
    print(response)


if __name__ == "__main__":
    main()