"""YAML settings loader for the agent template framework."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from schemas.settings import AgentSettings
from src.errors import FrameworkConfigurationError

DEFAULT_SETTINGS_PATH = Path(__file__).with_name("agent_template.yaml")


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FrameworkConfigurationError(f"Settings file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise FrameworkConfigurationError(
            f"Settings file must contain a YAML mapping: {path}"
        )

    return data


def load_agent_settings(path: str | Path | None = None) -> AgentSettings:
    """Load AgentSettings from YAML."""

    settings_path = Path(path) if path else DEFAULT_SETTINGS_PATH
    return AgentSettings.model_validate(_read_yaml(settings_path))
