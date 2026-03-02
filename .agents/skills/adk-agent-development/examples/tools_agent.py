"""Multi-Tool Agent (Codelab 2 Pattern).

Agent with FunctionTool, AgentTool (sub-agent), and LangchainTool.
Demonstrates the orchestrator/router pattern where root_agent delegates
to specialized tools based on user intent.

Reference: https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-empowering-with-tools
"""

import requests
from google.adk.agents import Agent
from google.adk.tools import FunctionTool, google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


# --- FunctionTool: Custom Python function ---
def get_fx_rate(base: str, target: str):
    """Fetches the current exchange rate between two currencies.

    Args:
        base: The base currency (e.g., "SGD").
        target: The target currency (e.g., "JPY").

    Returns:
        The exchange rate information as a json response, or None if the
        rate could not be fetched.
    """
    base_url = "https://hexarate.paikama.co/api/rates/latest"
    api_url = f"{base_url}/{base}?target={target}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()


# --- AgentTool: Sub-agent with Google Search ---
google_search_agent = Agent(
    model='gemini-2.5-flash',
    name='google_search_agent',
    description=(
        'A search agent that uses Google Search to get latest information '
        'about current events, weather, or business hours.'
    ),
    instruction=(
        'Use Google Search to answer user questions about real-time, '
        'logistical information.'
    ),
    tools=[google_search],
)


# --- LangchainTool: Wikipedia integration ---
langchain_wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=3000)
)
langchain_wikipedia_tool.description = (
    "Provides deep historical and cultural information on landmarks, "
    "concepts, and places. Use this for 'tell me about' or "
    "'what is the history of' type questions."
)


# --- Root Agent: Orchestrator ---
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    tools=[
        FunctionTool(get_fx_rate),
        AgentTool(agent=google_search_agent),
        LangchainTool(langchain_wikipedia_tool),
    ]
)
