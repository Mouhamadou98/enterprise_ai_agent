from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from src.config import settings  # adapte au vrai chemin de ton module Settings


class ElasticsearchClient:

    def __init__(self, url: str | None = None):
        self.client = Elasticsearch(url or settings.elasticsearch_url)

    def is_available(self) -> bool:
        return self.client.ping()

    def create_index(self, index_name: str, dimensions: int) -> None:

        if self.client.indices.exists(index=index_name):
            return 
        
        self.client.indices.create(
            index=index_name,
            mappings={
                "properties": {
                    "content": {
                        "type": "text",
                    },
                    "file_name": {
                        "type": "keyword",
                    },
                    "source": {
                        "type": "keyword",
                    },
                    "embedding": {
                        "type": "dense_vector",
                        "dims": dimensions,
                        "similarity": "cosine",
                    },
                }
            },
        )

    
    def index_document(self, index_name: str, content: str, embedding: list[float], metadata: dict) -> None:
            self.client.index(
                index=index_name,
                document={
                    "content": content,
                    "embedding": embedding,
                    "file_name": metadata.get("file_name"),
                    "source": metadata.get("source"),
                },
            )
    
    def bulk_index_documents(self, index_name: str, documents: list[dict]) -> int:

        actions = [
            {
                "_index": index_name,
                "_source": document,
            }
            for document in documents
        ]

        success, _ = bulk(
            self.client,
            actions,
        )

        return success
    
    def knn_search(self, index_name: str, query_vector: list[float], k: int = 5, num_candidates: int = 20) -> list[dict]:
        response = self.client.search(
            index=index_name,
            knn={
                "field": "embedding",
                "query_vector": query_vector,
                "k": k,
                "num_candidates": num_candidates,
            },
        )

        return [
            {
                "content": hit["_source"]["content"],
                "file_name": hit["_source"]["file_name"],
                "source": hit["_source"]["source"],
                "score": hit["_score"],
            }
            for hit in response["hits"]["hits"]
        ]
    
    def keyword_search(self, index_name: str, query: str, k: int = 5) -> list[dict]:
        
        response = self.client.search(
            index=index_name,
            size=k,
            query={
                "match": {
                    "content": query
                }
            },
        )

        return [
            {
                "content": hit["_source"]["content"],
                "file_name": hit["_source"]["file_name"],
                "source": hit["_source"]["source"],
                "score": hit["_score"],
            }
            for hit in response["hits"]["hits"]
        ]