"""Sanitized demo artifact schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class DemoStructure(BaseModel):
    source_path: str
    document_type: str = "generic_document"
    sections: list[str] = Field(default_factory=list)


class DemoItem(BaseModel):
    item_id: str
    label: str
    quantity: float
    unit: str


class DemoReportManifest(BaseModel):
    status: str
    source_path: str
    item_count: int
    artifact_paths: list[str]
