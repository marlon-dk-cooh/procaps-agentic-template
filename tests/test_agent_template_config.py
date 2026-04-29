from pathlib import Path

from config.loader import load_agent_settings


def test_load_agent_settings_flags(tmp_path: Path):
    config_path = tmp_path / "settings.yaml"
    config_path.write_text(
        """
agent:
  name: demo
  is_rag_required: true
  is_mcp_used: true
rag:
  provider: azure_search
  top_k: 3
mcp:
  servers: []
""",
        encoding="utf-8",
    )

    settings = load_agent_settings(config_path)

    assert settings.agent.name == "demo"
    assert settings.is_rag_required is True
    assert settings.is_mcp_used is True
    assert settings.rag.top_k == 3
