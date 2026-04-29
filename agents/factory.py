"""Factory for creating DeepAgents from sanitized framework specs."""

from __future__ import annotations

from typing import Any, Iterable

from mcp.loader import McpToolLoader
from rag.azure_search import build_azure_search_retriever
from schemas.agents import AgentSpec, SubAgentSpec
from schemas.settings import AgentSettings
from tools.rag_tools import build_retrieve_context_tool


def _create_deep_agent(**kwargs: Any) -> Any:
    """Import DeepAgents lazily so non-agent tests can run without the SDK."""

    from deepagents import create_deep_agent

    return create_deep_agent(**kwargs)


def _optional_capability_tools(
    settings: AgentSettings,
    rag_retriever: Any | None = None,
    mcp_loader: McpToolLoader | None = None,
) -> list[Any]:
    tools: list[Any] = []

    if settings.is_rag_required:
        retriever = rag_retriever or build_azure_search_retriever(settings.rag)
        tools.append(
            build_retrieve_context_tool(
                retriever=retriever,
                default_top_k=settings.rag.top_k,
            )
        )

    if settings.is_mcp_used:
        loader = mcp_loader or McpToolLoader()
        tools.extend(loader.load(settings.mcp))

    return tools


def _subagent_payloads(
    subagents: Iterable[SubAgentSpec],
    fallback_model: Any,
    extra_tools: list[Any],
) -> list[dict[str, Any]]:
    return [
        subagent.to_deepagents_dict(
            fallback_model=fallback_model,
            extra_tools=extra_tools,
        )
        for subagent in subagents
    ]


def create_agent_from_spec(
    spec: AgentSpec,
    settings: AgentSettings,
    *,
    rag_retriever: Any | None = None,
    mcp_loader: McpToolLoader | None = None,
) -> Any:
    """Create a DeepAgent from an AgentSpec and YAML-backed settings.

    Optional RAG and MCP tools are injected only when the settings flags request
    them. The supervisor itself stays lean and delegates work to subagents.
    """

    extra_tools = _optional_capability_tools(
        settings=settings,
        rag_retriever=rag_retriever,
        mcp_loader=mcp_loader,
    )

    return _create_deep_agent(
        system_prompt=spec.system_prompt,
        subagents=_subagent_payloads(
            subagents=spec.subagents,
            fallback_model=spec.model,
            extra_tools=extra_tools,
        ),
        model=spec.model,
    )
