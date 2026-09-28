from langchain_core.documents import Document

from src.rag.embeddings import EmbeddingService
from src.rag.elasticsearch_client import ElasticsearchClient
from src.rag.splitter import split_documents


class KnowledgeIndexer:
    def __init__( self, embedding_service: EmbeddingService, elasticsearch_client: ElasticsearchClient):
        self.embedding_service = embedding_service
        self.elasticsearch_client = elasticsearch_client

    def index_documents(self, documents: list[Document], index_name: str) -> int:
        chunks = split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]

        embeddings = self.embedding_service.embed_documents(texts)

        documents_to_index = []

        for chunk, embedding in zip(chunks, embeddings):
            documents_to_index.append(
                {
                    "content": chunk.page_content,
                    "embedding": embedding,
                    "file_name": chunk.metadata.get("file_name"),
                    "source": chunk.metadata.get("source"),
                }
            )

        return self.elasticsearch_client.bulk_index_documents(
            index_name=index_name,
            documents=documents_to_index,
        )