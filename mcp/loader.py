"""MCP tool loading boundary.

The first framework version defines the extension point without binding to a
specific MCP client implementation.
"""

from __future__ import annotations

from typing import Any

from schemas.settings import McpSettings
from src.errors import FrameworkConfigurationError

# Consume agent from Copilot Studio.
class McpToolLoader:
    """Loads MCP-provided tools when MCP is enabled."""

    def load(self, settings: McpSettings) -> list[Any]:
        if not settings.servers:
            return []

        raise FrameworkConfigurationError(
            "MCP server loading is scaffolded but no concrete MCP client is "
            "configured in this framework version."
        )
