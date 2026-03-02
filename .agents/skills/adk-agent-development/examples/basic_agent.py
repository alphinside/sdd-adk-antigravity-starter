"""Basic ADK Agent (Codelab 1 Pattern).

Minimal agent with just a model, name, and instruction.
Reference: https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation
"""

from google.adk.agents import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
