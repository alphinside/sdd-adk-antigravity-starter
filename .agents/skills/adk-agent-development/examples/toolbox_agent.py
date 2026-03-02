"""Toolbox Agent using MCP Toolbox for Databases (Codelab 5 Pattern).

Agent that loads database tools from an MCP Toolbox server.
All database logic lives in tools.yaml — no database code in the agent.

Reference: https://codelabs.developers.google.com/agentic-rag-toolbox-cloudsql
"""

import os
from google.adk.agents import LlmAgent
from toolbox_adk import ToolboxToolset

TOOLBOX_URL = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
toolbox = ToolboxToolset(TOOLBOX_URL)

root_agent = LlmAgent(
    name="jobs_agent",
    model="gemini-2.5-flash",
    instruction="""You are a helpful assistant at "TechJobs," a tech job listing platform.

Your job:
- Help developers browse job listings by role or tech stack.
- Provide full details about specific positions.
- Recommend jobs based on natural language descriptions of what the developer
  is looking for.

When a developer asks about a specific job by title or company, use the
get-job-details tool.
When a developer asks for a specific role category or tech stack, use the
search-jobs tool.
When a developer describes what kind of job they want — by interest area,
work style, or career goals — use the search-jobs-by-description tool for
semantic search.

Be conversational, knowledgeable, and concise.
""",
    tools=[toolbox],
)
