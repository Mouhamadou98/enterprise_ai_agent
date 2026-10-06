from src.tools.business_tools import BusinessTools
from src.llm.providers.ollama import OllamaLLM


class FakeService:

    def get_delivery(self, order_id):
        return {
            "order_id": order_id,
            "status": "IN_TRANSIT",
            "delay_days": 5,
        }


llm = OllamaLLM()

business_tools = BusinessTools(FakeService())

get_delivery = business_tools.get_delivery_tool()

messages = [
    {
        "role": "user",
        "content": "Donne-moi les informations de livraison de la commande ORD0001.",
    }
]

response = llm.generate_with_tools(
    messages=messages,
    tools=[get_delivery],
)

print(response)