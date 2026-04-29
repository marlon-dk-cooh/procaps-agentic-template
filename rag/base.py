"""Retriever protocol for RAG adapters."""

from __future__ import annotations

from typing import Protocol

from schemas.rag import RagQuery, RetrievedChunk


class Retriever(Protocol):
    def retrieve(self, query: RagQuery) -> list[RetrievedChunk]:
        """Return relevant chunks for a query."""
