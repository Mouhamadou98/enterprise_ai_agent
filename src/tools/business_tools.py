from langchain_core.tools import StructuredTool, tool

from src.services.acme_service import AcmeService
from src.rag.service import RAGService


class BusinessTools:

    def __init__(self, service: AcmeService, rag_service: RAGService | None = None):
        self.service = service
        self.rag_service = rag_service

    # def get_order(self, order_id: str) -> dict | None:
    #     """
    #     Récupère les informations d'une commande.

    #     Args:
    #         order_id: Identifiant de la commande.

    #     Returns:
    #         Les informations de la commande ou None si elle n'existe pas.
    #     """
    #     return self.service.get_order(order_id)
    
    # def get_order_tool(self) -> StructuredTool:
    #     return StructuredTool.from_function(
    #         func=self.get_order,
    #         name="get_order",
    #         description=(
    #             "Retrieve information about an order from the ACME Logistics ERP. "
    #             "Use this tool when the user asks about a specific order."
    #         ),
    #     )

    def get_order_tool(self):
        service = self.service

        @tool
        def get_order(order_id: str) -> dict | None:
            """Retrieve order information from the ACME Logistics ERP."""
            return service.get_order(order_id)

        return get_order
    
    def get_delivery_tool(self):

        service = self.service

        @tool
        def get_delivery(order_id: str) -> dict | None:
            """Retrieve delivery information for an order from the ACME Logistics ERP."""
            return service.get_delivery(order_id)

        return get_delivery
    
    def get_customer_incidents_tool(self):

        service = self.service

        @tool
        def get_customer_incidents(customer_id: str) -> list[dict]:
            """Retrieve all incidents previously reported by a customer."""
            return service.get_customer_incidents(customer_id)

        return get_customer_incidents
    
    def search_knowledge_base_tool(self):

        rag_service = self.rag_service

        @tool
        def search_knowledge_base(query: str) -> str:
            """Search the ACME Logistics internal knowledge base for procedures, policies, and business documentation."""

            if rag_service is None:
                raise RuntimeError("RAG service is not configured.")

            return rag_service.retrieve_context(
                query=query,
                k=5,
            )

        return search_knowledge_base
    
    def create_ticket_tool(self):
        
        service = self.service

        @tool
        def create_ticket(customer_id: str, order_id: str, incident_id: str, subject: str, priority: str = "MEDIUM") -> dict:
                
            """Create a support ticket for a customer order."""
            return service.create_ticket(
                customer_id=customer_id,
                order_id=order_id,
                incident_id=incident_id,
                subject=subject,
                priority=priority,
            )

        return create_ticket