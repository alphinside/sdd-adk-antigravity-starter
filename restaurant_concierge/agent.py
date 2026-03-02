"""Restaurant Concierge ADK Agent.

Pre-built starter agent with:
- Menu search (keyword + semantic via MCP Toolbox)
- Dietary preference tracking (via ToolContext)

Built from patterns in:
- Codelab 1: ADK Foundation
- Codelab 2: Persistent ADK with Cloud SQL
- Codelab 4: Agentic RAG with Toolbox
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from toolbox_core import ToolboxSyncClient

TOOLBOX_URL = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")

# Connect to MCP Toolbox for database tools (menu search)
toolbox_client = ToolboxSyncClient(TOOLBOX_URL)
toolbox_tools = toolbox_client.load_toolset()


async def save_dietary_preference(preference: str, ctx: ToolContext) -> str:
    """Save a dietary preference for the current user.

    Args:
        preference: The dietary preference to save (e.g., "vegetarian", "gluten-free").
    """
    preferences = ctx.state.get("dietary_preferences", [])
    if preference not in preferences:
        preferences.append(preference)
        ctx.state["dietary_preferences"] = preferences
    return f"Saved dietary preference: {preference}. Current preferences: {', '.join(preferences)}"


async def get_dietary_preferences(ctx: ToolContext) -> str:
    """Retrieve all saved dietary preferences for the current user."""
    preferences = ctx.state.get("dietary_preferences", [])
    if not preferences:
        return "No dietary preferences saved yet."
    return f"Current dietary preferences: {', '.join(preferences)}"


SYSTEM_INSTRUCTION = """You are a friendly and knowledgeable restaurant concierge for "The Cloud Kitchen."

Your capabilities:
- **Menu Search**: Search the menu by category, dietary requirements, or natural language queries.
  Use semantic search for questions like "something light and refreshing."
- **Dietary Preferences**: Remember and apply dietary preferences across the conversation.
  Always check saved preferences when recommending menu items.

Guidelines:
- Be warm and professional, like a real concierge at a fine dining restaurant.
- When recommending menu items, consider the guest's saved dietary preferences.
- For menu searches, use the search tools to find real items from the database — never make up
  menu items.
- Keep responses concise but informative.
- If a guest mentions a dietary restriction, proactively save it as a preference.
"""

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="restaurant_concierge",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        *toolbox_tools,
        save_dietary_preference,
        get_dietary_preferences,
    ],
)
