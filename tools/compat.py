"""Compatibility shims for optional LangChain/LangGraph imports."""

from __future__ import annotations

from typing import Any, Callable

try:
    from langchain_core.messages import ToolMessage
    from langchain_core.tools import InjectedToolCallId, tool
    from langgraph.prebuilt import InjectedState
    from langgraph.types import Command
except ImportError:
    class ToolMessage(dict):
        def __init__(self, content: str, tool_call_id: str = "") -> None:
            super().__init__(content=content, tool_call_id=tool_call_id)

    class Command(dict):
        def __init__(self, update: dict[str, Any] | None = None) -> None:
            super().__init__(update=update or {})
            self.update = update or {}

    class InjectedState:
        pass

    class InjectedToolCallId:
        pass

    def tool(description: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            func.description = description
            return func

        return decorator


__all__ = [
    "Command",
    "InjectedState",
    "InjectedToolCallId",
    "ToolMessage",
    "tool",
]
