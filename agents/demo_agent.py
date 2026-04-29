"""Runnable sanitized demo agent for LangGraph Studio."""

from __future__ import annotations

from agents.factory import create_agent_from_spec
from config.loader import load_agent_settings
from connections.llm import get_template_llm
from prompts.demo import (
    REPORT_BUILDER_AGENT_PROMPT,
    STRUCTURED_DOCUMENT_AGENT_PROMPT,
    build_demo_supervisor_prompt,
)
from schemas.agents import AgentSpec, SubAgentSpec
from tools.demo_tools import (
    build_demo_report,
    extract_demo_items,
    parse_document_source,
)


settings = load_agent_settings()
llm_model = get_template_llm()

structured_document_subagent = SubAgentSpec(
    name="structured_document_agent",
    description=(
        "Parses a user-provided document path into sanitized structured "
        "metadata and section artifacts."
    ),
    system_prompt=STRUCTURED_DOCUMENT_AGENT_PROMPT,
    tools=[parse_document_source],
    model=llm_model,
)

report_builder_subagent = SubAgentSpec(
    name="report_builder_agent",
    description=(
        "Reads structured document artifacts, extracts generic items, and "
        "produces a sanitized report manifest."
    ),
    system_prompt=REPORT_BUILDER_AGENT_PROMPT,
    tools=[extract_demo_items, build_demo_report],
    model=llm_model,
)

agent_template_spec = AgentSpec(
    name=settings.agent.name,
    system_prompt=build_demo_supervisor_prompt(settings),
    subagents=[structured_document_subagent, report_builder_subagent],
    model=llm_model,
)

agent_template_demo = create_agent_from_spec(
    spec=agent_template_spec,
    settings=settings,
)
