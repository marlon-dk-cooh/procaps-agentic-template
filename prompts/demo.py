"""Sanitized prompts for the template demo agent."""

from __future__ import annotations

from prompts.standard import STANDARD_DEEP_AGENT_INSTRUCTIONS
from schemas.settings import AgentSettings
from workflows.demo import DEMO_WORKFLOW_PLAYBOOK

STRUCTURED_DOCUMENT_AGENT_PROMPT = """
You are a structured document subagent.

Your job is to receive a document path and call `parse_document_source` once.
Return a concise summary of the virtual artifact you created. Do not infer
domain-specific facts and do not process real client data.
"""

REPORT_BUILDER_AGENT_PROMPT = """
You are a report builder subagent.

Your job is to read the sanitized structured document artifact, call
`extract_demo_items`, then call `build_demo_report`. Return the report manifest
path and the item count. Do not create real Excel files or client outputs.
"""


def build_demo_supervisor_prompt(settings: AgentSettings) -> str:
    capability_summary = (
        "Capability flags:\n"
        f"- is_rag_required: {settings.is_rag_required}\n"
        f"- is_mcp_used: {settings.is_mcp_used}\n"
    )

    return (
        "# Agent Template Demo Supervisor\n\n"
        + capability_summary
        + "\n"
        + DEMO_WORKFLOW_PLAYBOOK
        + "\n\n"
        + "=" * 80
        + "\n\n"
        + STANDARD_DEEP_AGENT_INSTRUCTIONS
    )
