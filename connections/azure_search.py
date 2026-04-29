"""Azure Search client construction."""

from __future__ import annotations

import os
from typing import Any

from schemas.settings import RagSettings
from src.errors import FrameworkConfigurationError


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise FrameworkConfigurationError(f"Missing required environment variable: {name}")
    return value


def create_search_client(settings: RagSettings) -> Any:
    """Create an Azure SearchClient for an existing index."""

    try:
        from azure.core.credentials import AzureKeyCredential
        from azure.search.documents import SearchClient
    except ImportError as exc:
        raise FrameworkConfigurationError(
            "Azure Search support requires azure-search-documents."
        ) from exc

    endpoint = _required_env(settings.endpoint_env)
    index_name = _required_env(settings.index_name_env)
    api_key = _required_env(settings.api_key_env)

    return SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(api_key),
    )
