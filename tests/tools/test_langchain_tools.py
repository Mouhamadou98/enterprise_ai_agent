from src.tools.business_tools import BusinessTools


class FakeService:

    def get_order(self, order_id: str):
        return {
            "order_id": order_id,
            "status": "SHIPPED",
        }


def test_get_order_langchain_tool():
    tools = BusinessTools(FakeService())

    tool = tools.get_order_tool()

    print(tool.name)
    print(tool.description)
    print(tool.args_schema.model_json_schema())

    result = tool.invoke({
        "order_id": "ORD0001"
    })

    assert result["order_id"] == "ORD0001"
    assert result["status"] == "SHIPPED"