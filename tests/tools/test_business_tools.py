from src.tools.business_tools import BusinessTools


class FakeService:

    def get_order(self, order_id: str):
        return {
            "order_id": order_id,
            "status": "SHIPPED",
        }


def test_get_order():
    tools = BusinessTools(FakeService())

    tool = tools.get_order_tool()

    assert tool.name == "get_order"

    result = tool.invoke({
        "order_id": "ORD0001"
    })

    assert result["order_id"] == "ORD0001"
    assert result["status"] == "SHIPPED"

def test_create_ticket_tool():
    class FakeService1:
        def create_ticket(
            self,
            customer_id,
            order_id,
            incident_id,
            subject,
            priority,
        ):
            return {
                "ticket_id": "TKT00001",
                "customer_id": customer_id,
                "order_id": order_id,
                "incident_id": incident_id,
                "subject": subject,
                "priority": priority,
                "status": "OPEN",
                "created_at": "2026-10-06",
            }

    tools = BusinessTools(FakeService1())

    tool = tools.create_ticket_tool()

    assert tool.name == "create_ticket"

    result = tool.invoke({
        "customer_id": "C0001",
        "order_id": "ORD0001",
        "incident_id": "INC0001",
        "subject": "Livraison en retard de 5 jours",
        "priority": "HIGH",
    })

    assert result["ticket_id"] == "TKT00001"
    assert result["customer_id"] == "C0001"
    assert result["order_id"] == "ORD0001"
    assert result["incident_id"] == "INC0001"
    assert result["subject"] == "Livraison en retard de 5 jours"
    assert result["priority"] == "HIGH"
    assert result["status"] == "OPEN"