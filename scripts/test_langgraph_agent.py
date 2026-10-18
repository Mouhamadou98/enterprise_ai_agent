from src.agents.graph import build_agent_graph
from src.repositories.acme_repository import AcmeRepository
from src.services.acme_service import AcmeService
from src.tools.business_tools import BusinessTools
from src.llm.factory import LLMFactory
from src.rag.embeddings import EmbeddingService
from src.rag.elasticsearch_client import ElasticsearchClient
from src.rag.retriever import KnowledgeRetriever
from src.rag.service import RAGService


repository = AcmeRepository()
service = AcmeService(repository)

embedding_service = EmbeddingService()
elasticsearch_client = ElasticsearchClient()

retriever = KnowledgeRetriever(
    embedding_service=embedding_service,
    elasticsearch_client=elasticsearch_client,
)

rag_service = RAGService(retriever=retriever)

business_tools = BusinessTools(
    service=service,
    rag_service=rag_service,
)

tools = [
    business_tools.get_order_tool(),
    business_tools.get_delivery_tool(),
    business_tools.get_customer_incidents_tool(),
    business_tools.search_knowledge_base_tool(),
]

llm = LLMFactory.create()

graph = build_agent_graph(
    llm=llm,
    tools=tools,
)

result = graph.invoke({
    "messages": [{
        "role": "user",
        "content": (
            "Que se passe-t-il avec la commande ORD00001 ? "
            "Quel est le statut de la livraison et quelles procédures "
            "internes doit-on consulter en cas de retard ?"
        ),
    }],
    "tool_calls": [],
})

print("\nRÉPONSE FINALE :")
print(result["messages"][-1]["content"])

# from pprint import pprint

# pprint(result["messages"])