"""Agent and subagent specification contracts."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SubAgentSpec(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    description: str
    system_prompt: str
    tools: list[Any] = Field(default_factory=list)
    model: Any | None = None

    def to_deepagents_dict(
        self,
        *,
        fallback_model: Any | None = None,
        extra_tools: list[Any] | None = None,
    ) -> dict[str, Any]:
        payload = {
            "name": self.name,
            "description": self.description,
            "system_prompt": self.system_prompt,
            "tools": [*self.tools, *(extra_tools or [])],
        }

        model = self.model or fallback_model
        if model is not None:
            payload["model"] = model

        return payload


class AgentSpec(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    system_prompt: str
    subagents: list[SubAgentSpec]
    model: Any
