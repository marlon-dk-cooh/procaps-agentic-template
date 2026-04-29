"""Prompt modules for the sanitized template agents."""

from prompts.demo import (
    REPORT_BUILDER_AGENT_PROMPT,
    STRUCTURED_DOCUMENT_AGENT_PROMPT,
    build_demo_supervisor_prompt,
)
from prompts.standard import STANDARD_DEEP_AGENT_INSTRUCTIONS

__all__ = [
    "REPORT_BUILDER_AGENT_PROMPT",
    "STANDARD_DEEP_AGENT_INSTRUCTIONS",
    "STRUCTURED_DOCUMENT_AGENT_PROMPT",
    "build_demo_supervisor_prompt",
]
