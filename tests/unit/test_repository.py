from src.repositories.acme_repository import AcmeRepository


def test_get_order():
    repository = AcmeRepository()

    order = repository.get_order("ORD02296")

    assert order is not None
    assert order["order_id"] == "ORD02296"
    assert order["customer_id"] != "C01112"
