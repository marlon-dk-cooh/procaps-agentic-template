"""State definitions for the template DeepAgents."""

from __future__ import annotations

from typing import Annotated, Any, Literal
from typing_extensions import NotRequired, TypedDict

try:
    from langchain.agents import AgentState
except ImportError:
    class AgentState(TypedDict, total=False):
        messages: list[Any]


class Todo(TypedDict):
    content: str
    status: Literal["pending", "in_progress", "completed"]


def file_reducer(left: dict[str, Any] | None, right: dict[str, Any] | None) -> dict[str, Any]:
    if left is None:
        return right or {}
    if right is None:
        return left
    return {**left, **right}


class AgentTemplateState(AgentState):
    todos: NotRequired[list[Todo]]
    files: NotRequired[Annotated[dict[str, Any], file_reducer]]
