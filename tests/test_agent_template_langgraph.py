import json
from pathlib import Path


def test_agent_template_demo_is_registered_in_langgraph_json():
    config = json.loads(Path("langgraph.json").read_text(encoding="utf-8"))

    assert (
        config["graphs"]["agent_template_demo"]
        == "./agent_template/agents/demo_agent.py:agent_template_demo"
    )
