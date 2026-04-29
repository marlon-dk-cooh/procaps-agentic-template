"""Workflow playbook for the sanitized demo agent."""

DEMO_WORKFLOW_PLAYBOOK = """
# Demo Workflow

When the user provides a document path, run two phases in sequence:

1. Delegate to `structured_document_agent` with the path. It must create
   `/demo/document_structure.json`.
2. Delegate to `report_builder_agent`. It must create `/demo/items.json` and
   `/demo/report_manifest.json`.

If RAG is enabled, subagents may call `retrieve_relevant_context` before
creating their final artifact. If MCP is enabled, use only the MCP tools loaded
by the framework. Report the final virtual artifact paths to the user.
"""
