from src.tools.business_tools import BusinessTools


class FakeService:

    def get_delivery(self, order_id: str):
        return {
            "order_id": order_id,
            "status": "IN_TRANSIT",
        }


def test_get_delivery_tool():
    tools = BusinessTools(FakeService())

    tool = tools.get_delivery_tool()

    assert tool.name == "get_delivery"

    result = tool.invoke({
        "order_id": "ORD0001"
    })

    assert result["order_id"] == "ORD0001"
    assert result["status"] == "IN_TRANSIT"