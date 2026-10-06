from src.tools.business_tools import BusinessTools



class FakeService:

    def get_customer_incidents(self, customer_id: str):
        return [
            {
                "incident_id": "INC001",
                "customer_id": customer_id,
                "status": "OPEN",
            },
            {
                "incident_id": "INC002",
                "customer_id": customer_id,
                "status": "CLOSED",
            },
        ]


def test_get_customer_incidents_tool():
    tools = BusinessTools(FakeService())

    tool = tools.get_customer_incidents_tool()

    assert tool.name == "get_customer_incidents"

    result = tool.invoke({
        "customer_id": "CUS001"
    })

    assert len(result) == 2
    assert result[0]["customer_id"] == "CUS001"
    assert result[1]["status"] == "CLOSED"