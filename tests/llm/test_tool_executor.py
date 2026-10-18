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



import pytest
from unittest.mock import Mock

from src.agents.tool_executor import ToolExecutor, ToolExecutionError


def test_execute_success():
    tool = Mock()
    tool.name = "get_delivery"
    tool.invoke.return_value = {"status": "DELIVERED"}

    executor = ToolExecutor([tool])

    result = executor.execute(
        "get_delivery",
        {"order_id": "ORD00001"},
    )

    assert result == {"status": "DELIVERED"}

    tool.invoke.assert_called_once_with(
        {"order_id": "ORD00001"}
    )


def test_execute_unknown_tool():
    executor = ToolExecutor([])

    with pytest.raises(ToolExecutionError, match="Unknown tool"):
        executor.execute("unknown_tool", {})


def test_execute_tool_failure():
    tool = Mock()
    tool.name = "get_delivery"
    tool.invoke.side_effect = ConnectionError(
        "Database unavailable"
    )

    executor = ToolExecutor([tool])

    with pytest.raises(ToolExecutionError, match="failed"):
        executor.execute(
            "get_delivery",
            {"order_id": "ORD00001"},
        )
