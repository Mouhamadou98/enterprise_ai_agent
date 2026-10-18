from src.rag.retriever import KnowledgeRetriever


class RAGService:

    def __init__(self, retriever: KnowledgeRetriever):
        self.retriever = retriever
    
    def retrieve_context(self, query: str, k: int = 5) -> str:
        """
        Retrieve relevant content from the knowledge base based on the query.

        Args:
            query (str): The input query for which to retrieve relevant content.
            k (int): The number of top results to retrieve. Default is 5.

        Returns:
            list[dict]: A list of dictionaries containing the retrieved content and metadata.
        """
        results = self.retriever.retrieve(query, k=k)

        if not results:
            return ""
        
        context_parts = []

        for result in results:
            context_parts.append(
                f"SOURCE: {result['file_name']}\n"
                f"{result['content']}"
            )
        
        return "\n\n---\n\n".join(context_parts)

    