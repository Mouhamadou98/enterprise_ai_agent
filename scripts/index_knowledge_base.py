from src.rag.embeddings import EmbeddingService
from src.rag.elasticsearch_client import ElasticsearchClient
from src.rag.indexer import KnowledgeIndexer
from src.rag.loader import DOCUMENTS_DIR, load_directory
from src.config import settings



INDEX_NAME = settings.elasticsearch_index


def main():
    documents = load_directory(DOCUMENTS_DIR)

    print(f"Documents chargés : {len(documents)}")

    embedding_service = EmbeddingService()
    elasticsearch_client = ElasticsearchClient()

    indexer = KnowledgeIndexer(
        embedding_service=embedding_service,
        elasticsearch_client=elasticsearch_client,
    )

    count = indexer.index_documents(
        documents=documents,
        index_name=INDEX_NAME,
    )

    print(f"Chunks indexés : {count}")


if __name__ == "__main__":
    main()