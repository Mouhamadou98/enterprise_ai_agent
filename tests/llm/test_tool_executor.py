from src.agents.tool_executor import ToolExecutor
from src.tools.business_tools import BusinessTools


def test_tool_executor():

    class FakeService:

        def get_delivery(self, order_id):
            return {
                "order_id": order_id,
                "status": "IN_TRANSIT",
            }

    business_tools = BusinessTools(FakeService())

    get_delivery = business_tools.get_delivery_tool()

    executor = ToolExecutor([
        get_delivery
    ])

    result = executor.execute(
        "get_delivery",
        {
            "order_id": "ORD0001"
        },
    )

    assert result["order_id"] == "ORD0001"
    assert result["status"] == "IN_TRANSIT"