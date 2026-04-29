"""Reusable DeepAgents operating instructions."""

STANDARD_DEEP_AGENT_INSTRUCTIONS = """
# Standard DeepAgents Instructions

Use the built-in planning and delegation tools for complex work:

- `write_todos` / `read_todos`: track multi-step objectives.
- `task`: delegate isolated work to configured subagents.
- `ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep`: inspect or
  manage the virtual filesystem when needed.

The supervisor should coordinate. Specialized subagents should perform the
domain work through their assigned tools. Prefer short, structured reports that
name the virtual artifacts produced.
"""
