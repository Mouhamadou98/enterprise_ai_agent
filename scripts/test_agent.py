from src.agents.tool_calling import ToolCallingAgent
from src.llm.providers.ollama import OllamaLLM
from src.tools.business_tools import BusinessTools


class FakeService:

    def get_delivery(self, order_id):
        return {
            "order_id": order_id,
            "status": "IN_TRANSIT",
            "delay_days": 5,
        }


llm = OllamaLLM()

business_tools = BusinessTools(FakeService())

tools = [
    business_tools.get_delivery_tool(),
]

agent = ToolCallingAgent(
    llm=llm,
    tools=tools,
)

response = agent.run(
    "Donne-moi les informations de livraison de la commande ORD0001."
)

print("\nFINAL RESPONSE:")
print(response)