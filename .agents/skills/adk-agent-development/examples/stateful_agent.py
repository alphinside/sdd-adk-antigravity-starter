"""Stateful Agent with ToolContext (Codelab 3 Pattern).

Smart Cafe Concierge that uses ToolContext for:
- Session-scoped state (current_order) — tied to the current conversation
- User-scoped state (user:dietary_preferences) — persists across all sessions

Reference: https://codelabs.developers.google.com/persistent-adk-cloudsql
"""

from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext

CAFE_MENU = {
    "espresso": {"price": 3.50, "description": "Rich and bold single shot", "tags": ["vegan", "dairy-free"]},
    "latte": {"price": 5.00, "description": "Espresso with steamed milk", "tags": ["gluten-free"]},
    "oat milk latte": {"price": 5.50, "description": "Espresso with steamed oat milk", "tags": ["vegan", "dairy-free"]},
    "cold brew": {"price": 4.00, "description": "Slow-steeped for 12 hours", "tags": ["vegan", "dairy-free"]},
    "croissant": {"price": 3.00, "description": "Buttery, flaky French pastry", "tags": []},
}


def get_menu() -> dict:
    """Returns the full cafe menu with prices, descriptions, and dietary tags.
    Use this tool when the customer asks what's available or wants to see the menu.
    """
    return CAFE_MENU


def place_order(tool_context: ToolContext, items: list[str]) -> dict:
    """Places an order for the specified menu items.

    Args:
        tool_context: Provided automatically by ADK.
        items: A list of menu item names the customer wants to order.
    """
    valid_items = []
    total = 0.0
    for item in items:
        item_lower = item.lower()
        if item_lower in CAFE_MENU:
            valid_items.append(item_lower)
            total += CAFE_MENU[item_lower]["price"]

    if not valid_items:
        return {"error": "None of those items are on our menu."}

    order = {"items": valid_items, "total": round(total, 2)}
    tool_context.state["current_order"] = order  # Session-scoped state
    return {"order": order}


def get_order_summary(tool_context: ToolContext) -> dict:
    """Returns the current order summary for this session.

    Args:
        tool_context: Provided automatically by ADK.
    """
    order = tool_context.state.get("current_order")
    if order:
        return {"order": order}
    return {"message": "No order has been placed yet in this session."}


def set_dietary_preference(tool_context: ToolContext, preference: str) -> dict:
    """Saves a dietary preference that persists across all conversations.

    Args:
        tool_context: Provided automatically by ADK.
        preference: The dietary preference to save (e.g., "vegan", "lactose intolerant").
    """
    existing = tool_context.state.get("user:dietary_preferences", [])
    if not isinstance(existing, list):
        existing = []
    preference_lower = preference.lower().strip()
    if preference_lower not in existing:
        existing.append(preference_lower)
    tool_context.state["user:dietary_preferences"] = existing  # User-scoped state
    return {"saved": preference_lower, "all_preferences": existing}


def get_dietary_preferences(tool_context: ToolContext) -> dict:
    """Retrieves the customer's saved dietary preferences.

    Args:
        tool_context: Provided automatically by ADK.
    """
    preferences = tool_context.state.get("user:dietary_preferences", [])
    if preferences:
        return {"preferences": preferences}
    return {"message": "No dietary preferences saved yet."}


root_agent = LlmAgent(
    name="cafe_concierge",
    model="gemini-2.5-flash",
    instruction="""You are a friendly and knowledgeable barista at "The Cloud Cafe".

Your job:
- Help customers browse the menu and answer questions about items.
- Take coffee and food orders.
- Remember and respect dietary preferences.

The customer's saved dietary preferences are: {user:dietary_preferences?}

IMPORTANT RULES:
- When a customer mentions a dietary restriction, ALWAYS save it using the
  set_dietary_preference tool before doing anything else.
- Before recommending items, check the customer's dietary preferences.
  Only recommend items compatible with those restrictions.
- When placing an order, confirm the items and total with the customer.

Be conversational, warm, and concise.
""",
    tools=[
        get_menu,
        place_order,
        get_order_summary,
        set_dietary_preference,
        get_dietary_preferences,
    ],
)
