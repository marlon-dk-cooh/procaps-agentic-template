"""Tool builders for optional RAG capabilities."""

from __future__ import annotations

import json
from typing import Any

from rag.base import Retriever
from schemas.rag import RagQuery
from tools.compat import tool


def build_retrieve_context_tool(
    retriever: Retriever,
    *,
    default_top_k: int = 5,
) -> Any:
    """Build a retrieval tool bound to a concrete retriever."""

    @tool(description="Retrieve relevant context from the configured RAG backend.")
    def retrieve_relevant_context(query: str, top_k: int | None = None) -> str:
        chunks = retriever.retrieve(
            RagQuery(
                query=query,
                top_k=top_k or default_top_k,
            )
        )
        return json.dumps(
            [chunk.model_dump() for chunk in chunks],
            sort_keys=True,
        )

    return retrieve_relevant_context
