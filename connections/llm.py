"""LLM construction for template agents."""

from __future__ import annotations

import os
import yaml
from pathlib import Path
from typing import Any

from src.errors import FrameworkConfigurationError
from connections.key_vault import resolve_secrets


def get_template_llm(max_tokens: int | None = None) -> Any:
    """Create the chat model used by the template demo by loading config and KV secrets."""

    try:
        from langchain.chat_models import init_chat_model
    except ImportError as exc:
        raise FrameworkConfigurationError(
            "LLM construction requires langchain to be installed."
        ) from exc

    config_path = Path(__file__).parent.parent / "config" / "services.yaml"
    if not config_path.exists():
        raise FrameworkConfigurationError(f"LLM config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    llms_config = config.get("llms", {})
    active_model_name = llms_config.get("default_model", "gpt4_reasoner")
    
    llm_config = llms_config.get(active_model_name, {})
    if not llm_config:
        raise FrameworkConfigurationError(f"Missing '{active_model_name}' config in services.yaml.")

    # Extract vault URL from the secrets block
    vault_url = config.get("secrets", {}).get("vault_url")

    # Resolve Key Vault secrets dynamically
    resolved_config = resolve_secrets(llm_config, vault_url=vault_url)

    provider = resolved_config.get("provider", "azure_openai")
    output_tokens = max_tokens or resolved_config.get("max_tokens", 2000)

    kwargs: dict[str, Any] = {
        "model": resolved_config.get("deployment_name", active_model_name),
        "model_kwargs": {"max_completion_tokens": output_tokens},
    }
    
    if "temperature" in resolved_config:
        kwargs["temperature"] = resolved_config["temperature"]

    # Since init_chat_model maps 'model_provider' to the correct Langchain class:
    if provider in ("azure_openai", "azure_foundry"):
        kwargs.update(
            {
                "model_provider": "azure_openai",
                "api_key": resolved_config.get("api_key"),
                "azure_endpoint": resolved_config.get("endpoint"),
                "api_version": resolved_config.get("api_version"),
                "deployment_name": resolved_config.get("deployment_name"),
            }
        )

    return init_chat_model(**kwargs)
