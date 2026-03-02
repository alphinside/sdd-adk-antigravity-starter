"""FastAPI Server for ADK Agent (Codelab 4 Pattern).

Production server wrapping the ADK agent with:
- Optional DatabaseSessionService via SESSION_SERVICE_URI
- Cloud Trace integration via trace_to_cloud=True
- Custom endpoint example (feedback)

Reference: https://codelabs.developers.google.com/deploy-manage-observe-adk-cloud-run
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from pydantic import BaseModel
from typing import Literal

load_dotenv()

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Get session service URI from environment variables
session_uri = os.getenv("SESSION_SERVICE_URI", None)

# Prepare arguments for get_fast_api_app
app_args = {
    "agents_dir": AGENT_DIR,
    "web": True,
    "trace_to_cloud": True,
}

# Only include session_service_uri if it's provided
if session_uri:
    app_args["session_service_uri"] = session_uri

# Create FastAPI app
app: FastAPI = get_fast_api_app(**app_args)
app.title = "my-agent"
app.description = "API for interacting with the ADK agent"


# Example: Custom endpoint for feedback collection
class Feedback(BaseModel):
    """Represents feedback for a conversation."""
    score: int | float
    text: str | None = ""
    invocation_id: str
    log_type: Literal["feedback"] = "feedback"


@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback."""
    # In production, log to Cloud Logging or a database
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
