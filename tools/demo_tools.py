"""Deterministic demo tools that emulate state-backed artifact flow."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Annotated, Any

from schemas.demo import DemoItem, DemoReportManifest, DemoStructure
from state.state import AgentTemplateState
from tools.compat import (
    Command,
    InjectedState,
    InjectedToolCallId,
    ToolMessage,
    tool,
)

STRUCTURE_PATH = "/demo/document_structure.json"
ITEMS_PATH = "/demo/items.json"
REPORT_PATH = "/demo/report_manifest.json"


def _artifact(data: dict[str, Any] | list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "data": data,
        "content": json.dumps(data, indent=2, sort_keys=True),
        "mime_type": "application/json",
        "modified_at": datetime.now(timezone.utc).isoformat(),
    }


def _files_from_state(state: AgentTemplateState | None) -> dict[str, Any]:
    return dict((state or {}).get("files", {}))


def _command(files: dict[str, Any], message: str, tool_call_id: str) -> Command:
    return Command(
        update={
            "files": files,
            "messages": [ToolMessage(message, tool_call_id=tool_call_id)],
        }
    )


def parse_document_source_impl(
    document_path: str,
    state: AgentTemplateState | None = None,
    tool_call_id: str = "",
) -> Command:
    files = _files_from_state(state)
    structure = DemoStructure(
        source_path=document_path,
        sections=["overview", "requirements", "outputs"],
    )
    files[STRUCTURE_PATH] = _artifact(structure.model_dump())

    return _command(
        files=files,
        message=f"Created sanitized structure artifact at {STRUCTURE_PATH}.",
        tool_call_id=tool_call_id,
    )


def extract_demo_items_impl(
    state: AgentTemplateState | None = None,
    tool_call_id: str = "",
) -> Command:
    files = _files_from_state(state)
    structure_entry = files.get(STRUCTURE_PATH, {})
    structure_data = structure_entry.get("data", {}) if isinstance(structure_entry, dict) else {}
    source_path = str(structure_data.get("source_path", "unknown"))

    items = [
        DemoItem(item_id="ITEM-001", label="Generic input", quantity=1, unit="unit"),
        DemoItem(item_id="ITEM-002", label="Generic review", quantity=1, unit="unit"),
        DemoItem(item_id="ITEM-003", label=f"Source reference: {source_path}", quantity=1, unit="file"),
    ]
    files[ITEMS_PATH] = _artifact([item.model_dump() for item in items])

    return _command(
        files=files,
        message=f"Created sanitized item artifact at {ITEMS_PATH}.",
        tool_call_id=tool_call_id,
    )


def build_demo_report_impl(
    state: AgentTemplateState | None = None,
    tool_call_id: str = "",
) -> Command:
    files = _files_from_state(state)
    structure_entry = files.get(STRUCTURE_PATH, {})
    items_entry = files.get(ITEMS_PATH, {})
    structure_data = structure_entry.get("data", {}) if isinstance(structure_entry, dict) else {}
    items_data = items_entry.get("data", []) if isinstance(items_entry, dict) else []

    manifest = DemoReportManifest(
        status="completed",
        source_path=str(structure_data.get("source_path", "unknown")),
        item_count=len(items_data) if isinstance(items_data, list) else 0,
        artifact_paths=[STRUCTURE_PATH, ITEMS_PATH, REPORT_PATH],
    )
    files[REPORT_PATH] = _artifact(manifest.model_dump())

    return _command(
        files=files,
        message=f"Created sanitized report manifest at {REPORT_PATH}.",
        tool_call_id=tool_call_id,
    )


@tool(description="Parse a document path into a sanitized structured artifact.")
def parse_document_source(
    document_path: str,
    state: Annotated[AgentTemplateState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId] = "",
) -> Command:
    return parse_document_source_impl(document_path, state, tool_call_id)


@tool(description="Extract deterministic generic items from the structured artifact.")
def extract_demo_items(
    state: Annotated[AgentTemplateState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId] = "",
) -> Command:
    return extract_demo_items_impl(state, tool_call_id)


@tool(description="Build a sanitized report manifest from demo artifacts.")
def build_demo_report(
    state: Annotated[AgentTemplateState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId] = "",
) -> Command:
    return build_demo_report_impl(state, tool_call_id)
