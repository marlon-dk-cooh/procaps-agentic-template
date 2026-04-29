from rag.azure_search import AzureSearchRetriever
from schemas.rag import RagQuery


class FakeSearchClient:
    def __init__(self):
        self.calls = []

    def search(self, **kwargs):
        self.calls.append(kwargs)
        return [
            {
                "content": "alpha",
                "title": "Doc A",
                "@search.score": 0.9,
            }
        ]


def test_azure_search_retriever_maps_results():
    client = FakeSearchClient()
    retriever = AzureSearchRetriever(client, default_top_k=2)

    chunks = retriever.retrieve(RagQuery(query="hello"))

    assert client.calls == [{"search_text": "hello", "top": 2}]
    assert chunks[0].content == "alpha"
    assert chunks[0].metadata == {"title": "Doc A"}
    assert chunks[0].score == 0.9
