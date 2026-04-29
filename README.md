# Agent Template

This folder is a sanitized framework scaffold that emulates the repository's
DeepAgents supervisor/subagent pattern without copying client-specific prompts,
data, documents, or database content.

The first demo graph follows this shape:

```text
supervisor
  -> structured_document_agent
  -> report_builder_agent
```

Optional capabilities are controlled by `config/agent_template.yaml`:

```yaml
agent:
  name: agent_template_demo
  is_rag_required: false
  is_mcp_used: false
```

When RAG is enabled, the framework queries an existing Azure Search index. It
does not create embeddings, FAISS/Chroma indexes, or ingestion jobs.
