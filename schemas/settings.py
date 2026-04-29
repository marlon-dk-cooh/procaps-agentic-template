"""YAML-backed framework settings."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class AgentFeatureSettings(BaseModel):
    name: str = "agent_template_demo"
    is_rag_required: bool = False
    is_mcp_used: bool = False


class RagSettings(BaseModel):
    provider: str = "azure_search"
    top_k: int = 5
    endpoint_env: str = "AZURE_SEARCH_ENDPOINT"
    index_name_env: str = "AZURE_SEARCH_INDEX_NAME"
    api_key_env: str = "AZURE_SEARCH_API_KEY"

    @field_validator("provider")
    @classmethod
    def provider_must_be_supported(cls, value: str) -> str:
        if value != "azure_search":
            raise ValueError("Only azure_search is supported in this scaffold.")
        return value


class McpSettings(BaseModel):
    servers: list[dict[str, Any]] = Field(default_factory=list)


class AgentSettings(BaseModel):
    agent: AgentFeatureSettings = Field(default_factory=AgentFeatureSettings)
    rag: RagSettings = Field(default_factory=RagSettings)
    mcp: McpSettings = Field(default_factory=McpSettings)

    @property
    def is_rag_required(self) -> bool:
        return self.agent.is_rag_required

    @property
    def is_mcp_used(self) -> bool:
        return self.agent.is_mcp_used
