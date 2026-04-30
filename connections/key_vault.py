"""Azure Key Vault secrets resolver."""

import os
import re
from typing import Any

try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
except ImportError:
    DefaultAzureCredential = None
    SecretClient = None


def resolve_secrets(config: dict[str, Any] | list[str] | str, vault_url: str | None = None) -> dict[str, Any]:
    """Recursively traverse a dict and replace ${KV-SecretName} with Azure Key Vault values."""
    kv_pattern = re.compile(r'\$\{KV-(.*?)\}', flags=re.IGNORECASE)
    client = None
    
    def _resolve(val: Any) -> Any:
        if isinstance(val, dict):
            return {k: _resolve(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [_resolve(item) for item in val]
        elif isinstance(val, str):
            matches = kv_pattern.findall(val)
            if matches:
                nonlocal client
                if not client:
                    v_url = vault_url or os.getenv("AZURE_KEY_VAULT_URL")
                    if not v_url:
                        raise ValueError(
                            "AZURE_KEY_VAULT_URL must be set in environment to resolve KV secrets."
                        )
                    if not DefaultAzureCredential:
                        raise ImportError(
                            "Please install `azure-identity` and `azure-keyvault-secrets` to use KV."
                        )
                    credential = DefaultAzureCredential()
                    client = SecretClient(vault_url=v_url, credential=credential)
                
                result = val
                for secret_name in matches:
                    secret = client.get_secret(secret_name)
                    # Use str(secret.value) safely if the secret contains values
                    result = result.replace(f"${{KV-{secret_name}}}", str(secret.value))
                return result
            return val
        return val

    return _resolve(config)
