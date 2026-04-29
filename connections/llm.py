"""LLM construction for template agents."""

from __future__ import annotations

import os
from typing import Any

from src.errors import FrameworkConfigurationError


def get_template_llm(max_tokens: int | None = None) -> Any:
    """Create the chat model used by the template demo.

    The defaults mirror the repository's Azure OpenAI style without importing
    project-specific agent modules.
    """

    try:
        from langchain.chat_models import init_chat_model
    except ImportError as exc:
        raise FrameworkConfigurationError(
            "LLM construction requires langchain to be installed."
        ) from exc

    model_name = os.getenv("AGENT_TEMPLATE_MODEL", "azure_openai:gpt-5.4-mini")
    output_tokens = max_tokens or int(os.getenv("AGENT_TEMPLATE_MAX_TOKENS", "4000"))

    kwargs: dict[str, Any] = {
        "model": model_name,
        "model_kwargs": {"max_completion_tokens": output_tokens},
    }

    if model_name.startswith("azure_openai:"):
        kwargs.update(
            {
                "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
                "deployment_name": os.getenv("AZURE_DEPLOYMENT_NAME"),
            }
        )

    return init_chat_model(**kwargs)
