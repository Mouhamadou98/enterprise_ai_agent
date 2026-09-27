from src.services.acme_service import AcmeService


class FakeRepository:

    def get_order(self, order_id):
        return {
            "order_id": order_id,
            "customer_id": "C0111",
            "status": "SHIPPED",
        }


def test_get_order():
    repository = FakeRepository()
    service = AcmeService(repository)

    result = service.get_order("ORD02296")

    assert result["order_id"] == "ORD02296"
    assert result["customer_id"] == "C0111"