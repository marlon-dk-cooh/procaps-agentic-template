from agents import factory
from schemas.agents import AgentSpec, SubAgentSpec
from schemas.rag import RetrievedChunk
from schemas.settings import AgentSettings


class FakeRetriever:
    def retrieve(self, query):
        return [RetrievedChunk(content=f"context:{query.query}", score=1.0)]


class FakeMcpLoader:
    def __init__(self):
        self.called = False

    def load(self, settings):
        self.called = True
        return [lambda: "mcp"]


def _spec():
    return AgentSpec(
        name="demo",
        system_prompt="supervisor",
        model=object(),
        subagents=[
            SubAgentSpec(
                name="worker",
                description="worker",
                system_prompt="worker prompt",
                tools=[],
            )
        ],
    )


def test_factory_omits_optional_tools(monkeypatch):
    captured = {}

    def fake_create_deep_agent(**kwargs):
        captured.update(kwargs)
        return "agent"

    monkeypatch.setattr(factory, "_create_deep_agent", fake_create_deep_agent)

    settings = AgentSettings.model_validate(
        {"agent": {"is_rag_required": False, "is_mcp_used": False}}
    )

    result = factory.create_agent_from_spec(_spec(), settings)

    assert result == "agent"
    assert captured["subagents"][0]["tools"] == []


def test_factory_injects_rag_and_mcp_tools(monkeypatch):
    captured = {}

    def fake_create_deep_agent(**kwargs):
        captured.update(kwargs)
        return "agent"

    monkeypatch.setattr(factory, "_create_deep_agent", fake_create_deep_agent)
    mcp_loader = FakeMcpLoader()
    settings = AgentSettings.model_validate(
        {"agent": {"is_rag_required": True, "is_mcp_used": True}}
    )

    factory.create_agent_from_spec(
        _spec(),
        settings,
        rag_retriever=FakeRetriever(),
        mcp_loader=mcp_loader,
    )

    assert mcp_loader.called is True
    assert len(captured["subagents"][0]["tools"]) == 2
