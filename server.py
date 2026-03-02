"""FastAPI server wrapping the ADK restaurant concierge agent.

Pre-built dev server with in-memory session storage.
"""

import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(web=True, agents_dir=".")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
