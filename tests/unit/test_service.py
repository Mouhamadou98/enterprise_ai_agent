from src.services.acme_service import AcmeService


class FakeRepository:

    def get_customer(self, customer_id: str):
        return {
            "customer_id": customer_id,
            "name": "Antoine Lefevre",
        }

    def get_delivery(self, order_id: str):
        return {
            "delivery_id": "DEL-ORD02296",
            "order_id": order_id,
            "status": "IN_TRANSIT",
        }

    def get_order_incidents(self, order_id: str):
        return [
            {
                "incident_id": "INC00001",
                "order_id": order_id,
                "status": "RESOLVED",
            }
        ]

    def get_invoice(self, order_id: str):
        return {
            "invoice_id": "INV02296",
            "order_id": order_id,
            "status": "PAID",
        }

    def get_customer_incidents(self, customer_id: str):
        return [
            {
                "incident_id": "INC00001",
                "customer_id": customer_id,
                "order_id": "ORD02296",
                "status": "RESOLVED",
            },
            {
                "incident_id": "INC01235",
                "customer_id": customer_id,
                "order_id": "ORD04265",
                "status": "RESOLVED",
            },
        ]
    
    def get_order(self, order_id: str):

        if order_id == "ORD99999":
            return None

        return {
            "order_id": order_id,
            "customer_id": "C0111",
            "status": "SHIPPED",
        }


def test_get_order_context():

    repository = FakeRepository()
    service = AcmeService(repository)

    result = service.get_order_context("ORD02296")

    assert result is not None

    assert result["order"]["order_id"] == "ORD02296"
    assert result["customer"]["customer_id"] == "C0111"

    assert result["delivery"]["order_id"] == "ORD02296"

    assert len(result["order_incidents"]) == 1
    assert result["order_incidents"][0]["order_id"] == "ORD02296"

    assert result["invoice"]["order_id"] == "ORD02296"

    assert len(result["customer_history"]) == 2

def test_get_order_context_order_not_found():

    repository = FakeRepository()
    service = AcmeService(repository)

    result = service.get_order_context("ORD99999")

    assert result is None
