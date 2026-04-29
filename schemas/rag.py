"""RAG query and retrieval contracts."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RagQuery(BaseModel):
    query: str
    top_k: int | None = None
    filters: dict[str, Any] = Field(default_factory=dict)


class RetrievedChunk(BaseModel):
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    score: float | None = None
