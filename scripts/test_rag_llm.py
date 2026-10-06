from src.llm.factory import LLMFactory
from src.llm.rag_service import RAGLLMService
from src.rag.embeddings import EmbeddingService
from src.rag.elasticsearch_client import ElasticsearchClient
from src.rag.retriever import KnowledgeRetriever
from src.rag.service import RAGService



def main():

    embedding_service = EmbeddingService()

    elasticsearch_client = ElasticsearchClient()

    retriever = KnowledgeRetriever(
        embedding_service=embedding_service,
        elasticsearch_client=elasticsearch_client,
    )

    rag_service = RAGService(
        retriever=retriever,
    )

    llm_service = LLMFactory.create()

    rag_llm_service = RAGLLMService(
        rag_service=rag_service,
        llm_service=llm_service,
    )

    question = "Que se passe-t-il si une livraison a 5 jours de retard ?"

    response = rag_llm_service.answer(
        question=question,
        k=5,
    )

    results = retriever.retrieve(
    query=question,
    k=10,
    )

    print("\n===== RETRIEVAL =====")

    for i, result in enumerate(results, start=1):
        print(f"\n--- {i} ---")
        print(f"Score : {result['score']}")
        print(f"Document : {result['file_name']}")
        print(f"Content : {result['content']}")

    print("\nQuestion :")
    print(question)

    print("\nRéponse :")
    print(response)


if __name__ == "__main__":
    main()