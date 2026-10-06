from src.tools.business_tools import BusinessTools


class FakeService:
    pass


class FakeRAGService:

    def retrieve_context(self, query: str, k: int = 5):
        return (
            "SOURCE: 01_delivery_policy.md\n"
            "Delay from 3 to 7 days: create a support ticket "
            "and notify the logistics team."
        )


def test_search_knowledge_base_tool():

    tools = BusinessTools(
        service=FakeService(),
        rag_service=FakeRAGService(),
    )

    tool = tools.search_knowledge_base_tool()

    assert tool.name == "search_knowledge_base"

    result = tool.invoke({
        "query": "What happens if a shipment is delayed for 5 days?"
    })

    assert "01_delivery_policy.md" in result
    assert "support ticket" in result