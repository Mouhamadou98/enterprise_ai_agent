from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticsearchClient:

    def __init__(self, url: str = "http://localhost:9200"):
        self.client = Elasticsearch(url)

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