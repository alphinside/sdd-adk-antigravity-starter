# TODO(codelab): Add YAML frontmatter above this line to activate the skill.
# Antigravity requires ---/name/description/--- to recognize a skill file.

# ADK Agent Development Skill

This skill guides you through building AI agents using Google's **Agent Development Kit (ADK)**. It synthesizes patterns from five production-ready codelabs covering the full agent development lifecycle.

## Source Codelabs

| # | Title | Key Topics |
|---|-------|------------|
| 1 | [ADK Foundation](https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation) | Project setup, basic agent, `adk run`/`adk web` |
| 2 | [Empowering with Tools](https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-empowering-with-tools) | FunctionTool, AgentTool (sub-agents), LangchainTool |
| 3 | [Persistent ADK with CloudSQL](https://codelabs.developers.google.com/persistent-adk-cloudsql) | ToolContext, state prefixes, DatabaseSessionService |
| 4 | [Deploy to Cloud Run](https://codelabs.developers.google.com/deploy-manage-observe-adk-cloud-run) | Dockerfile, FastAPI server, traffic management, Cloud Trace |
| 5 | [Agentic RAG with Toolbox](https://codelabs.developers.google.com/agentic-rag-toolbox-cloudsql) | MCP Toolbox, `tools.yaml`, ToolboxToolset, pgvector |

---

## 1. ADK Project Structure

ADK requires a specific directory layout. The agent directory must be a Python package with these mandatory files:

```
project-root/
├── my_agent/                # Agent package (directory name = agent name)
│   ├── __init__.py          # REQUIRED: makes it a Python package
│   ├── agent.py             # REQUIRED: defines root_agent
│   └── .env                 # OPTIONAL: env vars (loaded by adk CLI)
├── pyproject.toml           # Python project config
├── .env                     # Project-level env vars
└── .venv/                   # Virtual environment
```

### `__init__.py` — Module Registration

The `__init__.py` **must** import the agent module so ADK can discover `root_agent`:

```python
from . import agent
```

Or explicitly export:

```python
from my_agent.agent import root_agent
__all__ = ["root_agent"]
```

### `.env` — Environment Configuration

The `.env` file configures the Gemini backend. For **Vertex AI** (recommended for Google Cloud):

```env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

For **Google AI** (API key based):

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your-api-key
```

### Required Google Cloud APIs

When using Vertex AI, enable these APIs:

```bash
gcloud services enable aiplatform.googleapis.com
# For Cloud SQL persistence:
gcloud services enable sqladmin.googleapis.com compute.googleapis.com
# For Cloud Run deployment:
gcloud services enable run.googleapis.com artifactregistry.googleapis.com
```

---

## 2. Agent Definition Patterns

### Basic Agent (Codelab 1)

The simplest agent uses the `Agent` class with a model, name, and instruction:

```python
from google.adk.agents import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

**Key fields:**
- **`model`** — The Gemini model to use (e.g., `gemini-2.5-flash`, `gemini-2.5-pro`)
- **`name`** — Unique identifier for the agent. The variable MUST be named `root_agent`.
- **`description`** — Human-readable summary; also used by other agents in multi-agent systems to understand this agent's capabilities.
- **`instruction`** — System prompt that shapes the agent's persona and behavior. This is the most important field for controlling agent output.
- **`tools`** — List of tools the agent can invoke (see Section 3).

### Using `LlmAgent` (Codelab 3+)

`LlmAgent` is an alias/subclass of `Agent` used in later codelabs:

```python
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="cafe_concierge",
    model="gemini-2.5-flash",
    instruction="""You are a friendly barista at "The Cloud Cafe".
    Your job:
    - Help customers browse the menu.
    - Take coffee and food orders.
    - Remember and respect dietary preferences.
    """,
    tools=[get_menu, place_order],
)
```

> **Convention:** The agent instance variable **must** be named `root_agent` for ADK CLI tools (`adk run`, `adk web`) to discover it.

---

## 3. Tool Categories & Implementation

ADK supports four categories of tools. The agent's LLM reads tool **names** and **docstrings** to decide which tool to invoke.

### 3.1 FunctionTool — Custom Python Functions (Codelab 2)

Wrap any Python function as a tool. **Docstrings are critical** — the LLM uses them to understand when and how to call the tool.

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

def get_fx_rate(base: str, target: str):
    """Fetches the current exchange rate between two currencies.

    Args:
        base: The base currency (e.g., "SGD").
        target: The target currency (e.g., "JPY").

    Returns:
        The exchange rate information as a json response.
    """
    import requests
    base_url = "https://hexarate.paikama.co/api/rates/latest"
    api_url = f"{base_url}/{base}?target={target}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[FunctionTool(get_fx_rate)]
)
```

**Rules for FunctionTool:**
- Use clear, descriptive **function names** and **docstrings**
- Use **type hints** on all parameters — the LLM needs them to fill arguments correctly
- The `Args:` section in the docstring describes each parameter for the LLM
- Return structured data (dicts, lists) rather than formatted strings when possible
- Functions can also be passed directly in the `tools` list without wrapping in `FunctionTool()` — ADK will auto-wrap them

### 3.2 AgentTool — Sub-Agent Delegation (Codelab 2)

Package an entire agent as a tool for another agent. This creates a **multi-agent** architecture where the root agent orchestrates specialist sub-agents.

```python
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

# Specialist sub-agent
google_search_agent = Agent(
    model='gemini-2.5-flash',
    name='google_search_agent',
    description='A search agent that uses Google Search to get latest information.',
    instruction='Use Google Search to answer questions about real-time information.',
    tools=[google_search],
)

# Root agent delegates to the sub-agent
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant.',
    tools=[
        FunctionTool(get_fx_rate),
        AgentTool(agent=google_search_agent),
    ]
)
```

**Key patterns:**
- The root agent becomes an **orchestrator/router** — it understands request intent and delegates to the right tool
- The sub-agent's `description` is what the root agent reads to decide when to delegate
- `google_search` is a built-in ADK tool imported from `google.adk.tools`

### 3.3 LangchainTool — Third-Party Integration (Codelab 2)

Integrate tools from LangChain or other AI frameworks:

```python
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

langchain_wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=3000)
)
langchain_wikipedia_tool.description = (
    "Provides deep historical and cultural information on landmarks and places. "
    "Use this for 'tell me about' or 'what is the history of' type questions."
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant.',
    tools=[
        FunctionTool(get_fx_rate),
        AgentTool(agent=google_search_agent),
        LangchainTool(langchain_wikipedia_tool),
    ]
)
```

**Additional dependencies:** `pip install langchain-community wikipedia`

### 3.4 MCP Toolbox — Declarative Database Tools (Codelab 5)

Use **MCP Toolbox for Databases** to define database tools declaratively in YAML — no database code in your agent.

#### `tools.yaml` Configuration

The `tools.yaml` uses multi-document YAML (separated by `---`). Each document has `kind`, `name`, and `type` fields. Toolbox supports four resource kinds:

| `kind` | Purpose | Example `type` |
|--------|---------|----------------|
| `sources` | Database connections | `cloud-sql-postgres` |
| `embeddingModels` | Vector embedding models | `gemini` |
| `tools` | Agent-callable SQL tools | `postgres-sql` |
| `toolsets` | Named groups of tools | *(optional)* |

```yaml
# --- Data Source ---
kind: sources
name: my-db
type: cloud-sql-postgres
project: ${GOOGLE_CLOUD_PROJECT}
region: ${REGION}
instance: my-instance
database: my_db
user: postgres
password: ${DB_PASSWORD}
---
# --- Embedding Model ---
# Configures Toolbox to call Gemini for vector operations.
# Referenced by tools via `embeddedBy: gemini-embedding`.
kind: embeddingModels
name: gemini-embedding
type: gemini
model: gemini-embedding-001
dimension: 3072
---
# --- Tool 1: Keyword search ---
kind: tools
name: search-items
type: postgres-sql
source: my-db
description: >-
  Search items by category. Use empty string to match all.
statement: |
  SELECT title, category, description
  FROM items
  WHERE ($1 = '' OR LOWER(category) = LOWER($1))
  LIMIT 10
parameters:
  - name: category
    type: string
    description: "Category to filter by. Use empty string for all."
---
# --- Tool 2: Semantic search with embeddedBy ---
# `embeddedBy` tells Toolbox to auto-embed the search query text
# into a vector before executing the SQL. The agent sends plain text;
# Toolbox handles the embedding transparently.
kind: tools
name: search-by-description
type: postgres-sql
source: my-db
description: >-
  Find items matching a natural language description using vector similarity.
statement: |
  SELECT title, description,
    1 - (embedding <=> $1) AS similarity
  FROM items
  WHERE embedding IS NOT NULL
  ORDER BY embedding <=> $1
  LIMIT 5
parameters:
  - name: search_query
    type: string
    description: "Natural language description of what the user is looking for."
    embeddedBy: gemini-embedding
---
# --- Tool 3: Insert with automatic vector ingestion ---
# `valueFromParam` + `embeddedBy` enables transparent embedding on write:
# 1. Toolbox copies the `description` value into `description_vector`
# 2. Toolbox embeds that text into a vector via gemini-embedding
# 3. The LLM never sees this parameter — it's handled server-side
# Result: one tool call stores both raw text AND its embedding.
kind: tools
name: add-item
type: postgres-sql
source: my-db
description: >-
  Add a new item to the platform.
statement: |
  INSERT INTO items (title, description, embedding)
  VALUES ($1, $2, $3)
  RETURNING title
parameters:
  - name: title
    type: string
    description: "The item title."
  - name: description
    type: string
    description: "A short description."
  - name: description_vector
    type: string
    description: "Auto-generated embedding vector."
    valueFromParam: description
    embeddedBy: gemini-embedding
```

**Key `tools.yaml` parameter features:**
- **`embeddedBy`** — Auto-embeds the parameter value using the named embedding model before SQL execution. Used on search queries so the agent sends text but the query uses vectors.
- **`valueFromParam`** — Copies the value from another parameter into this one. Combined with `embeddedBy`, this enables transparent vector ingestion on writes without the LLM knowing about embeddings.

#### Agent Code with ToolboxToolset

```python
import os
from google.adk.agents import LlmAgent
from toolbox_adk import ToolboxToolset

TOOLBOX_URL = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
toolbox = ToolboxToolset(TOOLBOX_URL)

root_agent = LlmAgent(
    name="jobs_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant...",
    tools=[toolbox],
)
```

**Dependencies:** `pip install google-adk toolbox-adk`

**Running the Toolbox server locally:**

```bash
# Download and make executable
curl -O https://storage.googleapis.com/genai-toolbox/v0.27.0/linux/amd64/toolbox
chmod +x toolbox

# Start (requires env vars for database + embedding model)
export GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT
export GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION
export GOOGLE_GENAI_USE_VERTEXAI=true
export DB_PASSWORD=$DB_PASSWORD
export REGION=$REGION
./toolbox --tools-file tools.yaml
```

> **Note:** `GOOGLE_GENAI_USE_VERTEXAI` and `GOOGLE_CLOUD_LOCATION` are required when `tools.yaml` includes an `embeddingModels` resource — they tell the Gemini SDK to route through Vertex AI.

> **Alternative client:** You can also use `toolbox_core.ToolboxSyncClient` to load tools:
> ```python
> from toolbox_core import ToolboxSyncClient
> client = ToolboxSyncClient(TOOLBOX_URL)
> toolbox_tools = client.load_toolset()
> # Then use: tools=[*toolbox_tools, other_tools...]
> ```

---

## 4. Stateful Agents — ToolContext & State Management (Codelab 3)

### Understanding Session Events vs State

- **Events** — Immutable chronological log (every message, response, tool call). Think: *conversation transcript*.
- **State** — Mutable key-value scratchpad. Think: *sticky notes beside the transcript*.

### ToolContext Injection

ADK automatically injects `ToolContext` into any tool function that declares it as a parameter. You never create it yourself.

```python
from google.adk.tools import ToolContext

def place_order(tool_context: ToolContext, items: list[str]) -> dict:
    """Places an order for the specified menu items.

    Args:
        tool_context: Provided automatically by ADK.
        items: A list of menu item names to order.
    """
    order = {"items": items, "total": calculate_total(items)}
    tool_context.state["current_order"] = order  # Write to session state
    return {"order": order}

def get_order(tool_context: ToolContext) -> dict:
    """Returns the current order summary."""
    order = tool_context.state.get("current_order")  # Read from session state
    if order:
        return {"order": order}
    return {"message": "No order placed yet."}
```

### State Prefixes

State keys use prefixes to control their **scope**:

| Prefix | Scope | Survives restart (with DB)? | Example |
|--------|-------|----------------------------|---------|
| *(none)* | Current session only | Yes | `current_order` |
| `user:` | All sessions for this user | Yes | `user:dietary_preferences` |
| `app:` | All sessions, all users | Yes | `app:global_settings` |
| `temp:` | Current invocation only | No | `temp:intermediate_result` |

```python
def set_dietary_preference(tool_context: ToolContext, preference: str) -> dict:
    """Saves a dietary preference that persists across all conversations."""
    existing = tool_context.state.get("user:dietary_preferences", [])
    if preference.lower() not in existing:
        existing.append(preference.lower())
    tool_context.state["user:dietary_preferences"] = existing
    return {"saved": preference, "all_preferences": existing}
```

### State Injection in Instructions

Reference state values directly in the agent's `instruction` using `{key?}` syntax:

```python
root_agent = LlmAgent(
    name="cafe_concierge",
    model="gemini-2.5-flash",
    instruction="""You are a friendly barista.
    The customer's dietary preferences are: {user:dietary_preferences?}

    IMPORTANT: When a customer mentions a dietary restriction,
    ALWAYS save it using the set_dietary_preference tool first.
    """,
    tools=[get_menu, place_order, set_dietary_preference, get_dietary_preferences],
)
```

> **Note:** The `?` suffix in `{user:dietary_preferences?}` prevents an error if the key doesn't exist yet.

---

## 5. Session Persistence with Cloud SQL (Codelab 3)

### Default: Local Storage

By default, `adk web` stores sessions in a local SQLite database at `<agent_dir>/.adk/session.db`. This is lost on serverless restarts.

### Production: DatabaseSessionService with PostgreSQL

For persistent memory across restarts, use Cloud SQL PostgreSQL:

#### 1. Create a Cloud SQL instance

```bash
gcloud sql instances create my-agent-db \
  --database-version=POSTGRES_17 \
  --edition=ENTERPRISE \
  --region=us-central1 \
  --tier=db-f1-micro \
  --root-password=${DB_PASSWORD} \
  --quiet
```

#### 2. Create a database

```bash
gcloud sql databases create agent_db --instance=my-agent-db
```

#### 3. Connect via Cloud SQL Auth Proxy

```bash
# Download proxy
curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.15.2/cloud-sql-proxy.linux.amd64
chmod +x cloud-sql-proxy

# Start proxy (runs in background)
./cloud-sql-proxy ${GOOGLE_CLOUD_PROJECT}:us-central1:my-agent-db &
```

#### 4. Configure the agent to use DatabaseSessionService

Set in `.env` or environment:

```env
SESSION_SERVICE_URI=postgresql+asyncpg://postgres:${DB_PASSWORD}@127.0.0.1:5432/agent_db
```

Or pass to FastAPI server:

```python
from google.adk.cli.fast_api import get_fast_api_app

session_uri = os.getenv("SESSION_SERVICE_URI")
app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    session_service_uri=session_uri,
)
```

---

## 6. Running & Testing Locally (Codelab 1)

### CLI Mode

```bash
adk run my_agent
# or with uv:
uv run adk run my_agent
```

### Development Web UI

```bash
adk web
# or with custom port:
uv run adk web --port 8080
```

The web UI provides:
- Chat interface with Markdown rendering
- **Events tab** — inspect each function call, tool response, and agent reasoning
- **State tab** — view current session state values
- Agent dropdown to select from multiple agents in the directory

### Creating an Agent via CLI

```bash
adk create my_agent
# Or non-interactively:
uv run adk create my_agent \
  --model gemini-2.5-flash \
  --project ${GOOGLE_CLOUD_PROJECT} \
  --region ${GOOGLE_CLOUD_LOCATION}
```

---

## 7. Deployment to Cloud Run (Codelab 4)

### FastAPI Server (`server.py`)

Wrap the ADK agent in a FastAPI app using `get_fast_api_app`:

```python
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

load_dotenv()

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
session_uri = os.getenv("SESSION_SERVICE_URI", None)

app_args = {"agents_dir": AGENT_DIR, "web": True, "trace_to_cloud": True}
if session_uri:
    app_args["session_service_uri"] = session_uri

app: FastAPI = get_fast_api_app(**app_args)
app.title = "my-agent"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Dockerfile

```dockerfile
FROM python:3.12-slim
RUN pip install --no-cache-dir uv==0.7.13
WORKDIR /app
COPY . .
RUN uv sync --frozen
EXPOSE 8080
CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Deploy Command

```bash
gcloud run deploy my-agent \
  --source . \
  --port 8080 \
  --project ${GOOGLE_CLOUD_PROJECT} \
  --allow-unauthenticated \
  --add-cloudsql-instances ${DB_CONNECTION_NAME} \
  --update-env-vars SESSION_SERVICE_URI="postgresql+pg8000://postgres:password@postgres/?unix_sock=/cloudsql/${DB_CONNECTION_NAME}/.s.PGSQL.5432",GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT} \
  --region us-central1 \
  --min 1 \
  --memory 1G \
  --concurrency 10
```

### Traffic Management (Gradual Rollout)

Deploy a new revision without taking traffic, then gradually shift:

```bash
# Deploy with no-traffic flag
gcloud run deploy my-agent --source . --no-traffic ...

# Split traffic: 90% old, 10% new
gcloud run services update-traffic my-agent \
  --to-revisions LATEST=10 --region us-central1

# Full rollout
gcloud run services update-traffic my-agent \
  --to-latest --region us-central1
```

### Cloud Trace Integration

Enable tracing via the `trace_to_cloud=True` parameter in `get_fast_api_app`. Traces are sent to **Google Cloud Trace** and provide end-to-end visibility into agent invocations.

```bash
# Enable Cloud Trace API
gcloud services enable cloudtrace.googleapis.com
```

---

## 8. Quick Reference: Common Imports

```python
# Core agent
from google.adk.agents import Agent, LlmAgent

# Tool types
from google.adk.tools import FunctionTool, ToolContext
from google.adk.tools import google_search          # Built-in Google Search
from google.adk.tools.agent_tool import AgentTool    # Sub-agent as tool
from google.adk.tools.langchain_tool import LangchainTool  # LangChain tools

# MCP Toolbox
from toolbox_adk import ToolboxToolset
from toolbox_core import ToolboxSyncClient

# FastAPI server
from google.adk.cli.fast_api import get_fast_api_app
```

---

## 9. Common Dependencies

```toml
# pyproject.toml or pip install
[project]
dependencies = [
    "google-adk>=1.25.0",     # Core ADK
    "asyncpg",                 # For DatabaseSessionService
    "toolbox-adk>=0.6.0",     # MCP Toolbox integration (if using database tools)
    "langchain-community",     # For LangChain tool integration
    "python-dotenv",           # For .env loading in custom servers
]
```

---

## 10. Checklist: Building a New ADK Agent

1. **Create project structure** — `adk create <agent_name>` or manually create the directory with `__init__.py`, `agent.py`, `.env`
2. **Configure `.env`** — Set `GOOGLE_GENAI_USE_VERTEXAI`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`
3. **Define `root_agent`** in `agent.py` — Choose model, write instruction, add tools
4. **Implement tools** — Use FunctionTool for custom logic, AgentTool for sub-agents, ToolboxToolset for database access
5. **Add state management** (if needed) — Use `ToolContext` with appropriate state prefixes
6. **Test locally** — `adk web` for interactive testing
7. **Add persistence** (if needed) — Set up Cloud SQL + `DatabaseSessionService`
8. **Create `server.py`** — Wrap with `get_fast_api_app()` for production deployment
9. **Deploy** — Dockerfile + `gcloud run deploy`
10. **Enable observability** — `trace_to_cloud=True` for Cloud Trace
