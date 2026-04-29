"""Azure Search retriever for an existing search index."""

from __future__ import annotations

from typing import Any

from connections.azure_search import create_search_client
from rag.base import Retriever
from schemas.rag import RagQuery, RetrievedChunk
from schemas.settings import RagSettings


class AzureSearchRetriever(Retriever):
    """Retrieve chunks from an existing Azure Search index."""

    def __init__(
        self,
        client: Any,
        *,
        default_top_k: int = 5,
        content_fields: list[str] | None = None,
    ) -> None:
        self._client = client
        self._default_top_k = default_top_k
        self._content_fields = content_fields or ["content", "text", "chunk"]

    def retrieve(self, query: RagQuery) -> list[RetrievedChunk]:
        top_k = query.top_k or self._default_top_k
        results = self._client.search(search_text=query.query, top=top_k)
        return [self._to_chunk(result) for result in results]

    def _to_chunk(self, result: Any) -> RetrievedChunk:
        raw = dict(result) if not isinstance(result, dict) else result
        content = ""
        for field in self._content_fields:
            value = raw.get(field)
            if value:
                content = str(value)
                break

        score = raw.get("@search.score") or raw.get("score")
        metadata = {
            key: value
            for key, value in raw.items()
            if key not in self._content_fields and not key.startswith("@search.")
        }

        return RetrievedChunk(content=content, metadata=metadata, score=score)


def build_azure_search_retriever(settings: RagSettings) -> AzureSearchRetriever:
    return AzureSearchRetriever(
        client=create_search_client(settings),
        default_top_k=settings.top_k,
    )
