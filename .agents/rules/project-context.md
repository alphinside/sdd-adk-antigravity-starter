# Project Context: Restaurant Concierge

**Last Updated**: 2026-06-06
**Updated By**: Feature 001-table-reservation-api

## Project Identity

- **Name**: Restaurant Concierge (`sdd-adk-agents-agy`)
- **Type**: web-app
- **Purpose**: A starter restaurant concierge application powered by a Google ADK agent. It supports menu searches (using both keyword and semantic searches) and dietary preference tracking.
- **Domain**: Food & Beverage / Hospitality / Virtual Concierge

## Technology Stack

### Languages & Versions
- **Python**: `>=3.12` (added by `main`)
- **SQL (PostgreSQL Dialect)**: `17` (added by `main`)

### Frameworks & Libraries
- **google-adk**: `>=1.0.0` (added by `main`)
- **toolbox-core**: `>=1.0.0` (added by `main`)
- **google-genai**: `>=1.0.0` (added by `main`)
- **cloud-sql-python-connector[pg8000]**: `>=1.0.0` (added by `main`)
- **uvicorn**: `>=0.30.0` (added by `main`)
- **antigravity**: `>=0.1` (added by `main`)
- **FastAPI**: Transitive dependency via `google-adk` (added by `main`)

### Storage
- **Cloud SQL PostgreSQL**: `17` with `vector` and `google_ml_integration` extensions enabled (added by `main`)

### Testing
- **pytest**: For unit, integration, and BDD endpoint testing (added by `001-table-reservation-api`)

## Project Structure

```
├── .agents/
│   ├── rules/
│   │   ├── .gitkeep
│   │   └── project-context.md
│   ├── skills/
│   │   ├── cavecrew/
│   │   │   ├── README.md
│   │   │   └── SKILL.md
│   │   ├── mcp-toolbox-postgres/
│   │   │   └── SKILL.md
│   │   └── repo-research/
│   │       └── SKILL.md
│   └── workflows/
│       ├── speckit.analyze.md
│       ├── speckit.checklist.md
│       ├── speckit.clarify.md
│       ├── speckit.constitution.md
│       ├── speckit.implement.md
│       ├── speckit.plan.md
│       ├── speckit.specify.md
│       └── speckit.tasks.md
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   ├── scripts/
│   │   └── bash/
│   │       ├── check-prerequisites.sh
│   │       ├── common.sh
│   │       ├── create-new-feature.sh
│   │       └── setup-plan.sh
│   └── templates/
│       ├── checklist-template.md
│       ├── plan-template.md
│       ├── project-context-template.md
│       ├── spec-template.md
│       └── tasks-template.md
├── restaurant_concierge/
│   ├── __init__.py
│   ├── agent.py
│   ├── database.py
│   ├── models.py
│   └── reservations.py
├── scripts/
│   ├── seed_db.py
│   └── setup_database.sh
├── tests/
│   ├── conftest.py
│   └── test_reservations.py
├── .env.example
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
├── server.py
├── skills-lock.json
├── tools.yaml
└── uv.lock
```

## API Surface

| Method | Path | Purpose |
|--------|------|---------|
| GET/POST | `/` | Web chat interface / health check (default FastAPI app wrapper provided by `google-adk`) |
| POST | `/api/chat` | Behind-the-scenes endpoint (if applicable) for chat interaction with the agent |
| POST | `/reservations` | Create a new table reservation |
| GET | `/reservations` | List all reservations (secured with X-API-KEY header) |

## Runtime Dependency Graph

```
[FastAPI Server :8080] → [MCP Toolbox :5000] → [Cloud SQL (PostgreSQL 17)] → [Vertex AI]
```

- **FastAPI Server (`server.py`)**: Runs on port `8080`. Serves the web-based chat interface. Started via `uv run python server.py`.
- **MCP Toolbox (`tools.yaml`)**: Runs on port `5000`. Exposes PostgreSQL database queries as tool definitions to the LLM agent. Started via `npx -y @toolbox-sdk/server --config tools.yaml`.
- **Cloud SQL (PostgreSQL 17)**: Managed relational database storing menu items and vector embeddings.
- **Vertex AI**: Google Cloud AI platform, accessed directly within the database via the `google_ml_integration` extension to generate text embeddings using `gemini-embedding-001`.

## Local Dev Runbook

1. **Configure Environment Variables**: Copy `.env.example` to `.env` and fill in:
   - `GOOGLE_CLOUD_PROJECT`
   - `REGION`
   - `DB_PASSWORD`
2. **Install Dependencies**: Install the project dependencies and environment using `uv`:
   ```bash
   uv sync
   ```
3. **Database Setup & Seeding**: Create the Cloud SQL database instance, enable vector/ML extensions, seed initial menu items, and generate embeddings:
   ```bash
   bash scripts/setup_database.sh
   ```
   *(Note: This script also starts the MCP Toolbox in the background.)*
4. **Start the FastAPI Server**: Start the local concierge agent server:
   ```bash
   uv run python server.py
   ```
5. **Open URL**: Navigate to [http://localhost:8080](http://localhost:8080) to interact with the concierge.

## Data Model Overview

### Entities (Cross-Feature)
- **menu_items** (defined in `main`):
  - Purpose: Stores the list of menu items available at the restaurant.
  - Key fields:
    - `id` (`SERIAL PRIMARY KEY`)
    - `name` (`VARCHAR(255) NOT NULL`)
    - `category` (`VARCHAR(100) NOT NULL`)
    - `description` (`TEXT NOT NULL`)
    - `price` (`DECIMAL(10, 2) NOT NULL`)
    - `dietary_tags` (`TEXT[] DEFAULT '{}'`)
    - `embedding` (`vector(3072)`)
    - `created_at` (`TIMESTAMP DEFAULT CURRENT_TIMESTAMP`)
  - Relationships: None.
  - Special features: Has a vector embedding column mapped to the 3072-dimensional Vertex AI embedding model `gemini-embedding-001`.

- **reservations** (defined in `001-table-reservation-api`):
  - Purpose: Stores customer table reservations.
  - Key fields:
    - `id` (`SERIAL PRIMARY KEY`)
    - `customer_name` (`VARCHAR(255) NOT NULL`)
    - `email` (`VARCHAR(255) NOT NULL`)
    - `phone` (`VARCHAR(50) NOT NULL`)
    - `party_size` (`INTEGER NOT NULL`)
    - `reservation_date` (`DATE NOT NULL`)
    - `reservation_time` (`TIME NOT NULL`)
    - `created_at` (`TIMESTAMP DEFAULT CURRENT_TIMESTAMP`)
  - Relationships: None.
  - Special features: Requires transaction-level serialization or row-level locking to prevent capacity limit (40 seats) overbooking.

### Tool Definitions
- **search_menu**: `menu_items` — SELECT (keyword match on name, category, or description)
- **semantic_search_menu**: `menu_items` — SELECT (vector distance cosine similarity search)
- **get_menu_by_category**: `menu_items` — SELECT (filter by category)
- **save_dietary_preference**: Python-based tool saving preference in conversation context (`ToolContext.state`)
- **get_dietary_preferences**: Python-based tool retrieving preferences from conversation context (`ToolContext.state`)

## Domain Glossary

| Term | Definition |
|------|-----------|
| **ADK** | Agent Development Kit, a Google-designed framework for building AI agents with tool-calling capabilities. |
| **MCP Toolbox** | Model Context Protocol server that wraps database connections and queries as standardized tools. |
| **google_ml_integration** | Cloud SQL extension that enables executing ML predictions and embedding generation directly via SQL commands. |
| **pgvector** | PostgreSQL extension enabling vector type storage and high-speed nearest-neighbor similarity searches. |

## External Integrations

- **Vertex AI (gemini-embedding-001)**: Generates text embeddings for menu searches and data seeding (added by `main`).
  - Authentication: Application Default Credentials (ADC) or service account permissions (`roles/aiplatform.user`) bound to the Cloud SQL instance service account.
  - Endpoints: Accessed via standard Cloud SQL `google_ml_integration.embedding(...)` function.

## Development Workflow

- **Branch Strategy**: Feature branches numbered `###-feature-name`.
- **Commit Convention**: No strict commit convention established yet.
- **Build Command**: `uv sync`
- **Test Command**: None configured yet.
- **Lint Command**: None configured yet.

## Architecture Patterns

- **Code Organization**: Feature-based codebase. The agent definition lies in `restaurant_concierge/agent.py`, database seeding in `scripts/`, MCP tool definitions in `tools.yaml`, and FastAPI server wrapper in `server.py`.
- **Error Handling**: Relies on standard Python try-except structures and FastAPI error processing.
- **State Management**: Conversational state (like dietary preferences) is saved using `ToolContext.state` in the ADK agent, preserving preferences during a session.
- **Naming Conventions**: standard Python PEP 8 (snake_case for functions/files, PascalCase for classes).

## Recent Features

- **001-table-reservation-api**: Added table reservations API (POST/GET) with static seating capacity checks and API key security.
- **main**: Added core restaurant concierge agent, menu search tools (keyword + semantic via MCP Toolbox), dietary preference tracking, and database seed scripts.

## Configuration

- **Config Files**:
  - `pyproject.toml` (Python packages & configurations)
  - `tools.yaml` (MCP database source and tool query mappings)
  - `.env` (Environment secrets and setup parameters)

### Environment Variable Dependency Chain

| Variable | Consumed By | What Breaks If Missing |
|----------|-------------|----------------------|
| `GOOGLE_CLOUD_PROJECT` | `setup_database.sh`, `tools.yaml`, `seed_db.py` | Google Cloud SQL creation, Vertex AI calls, and database setup will fail. |
| `REGION` | `setup_database.sh`, `tools.yaml`, `seed_db.py` | Database connection or instance creation will fail. |
| `DB_PASSWORD` | `setup_database.sh`, `tools.yaml`, `seed_db.py` | Authentication to Cloud SQL Postgres instance will fail. |
| `TOOLBOX_URL` | `restaurant_concierge/agent.py` | Agent will fail to load or connect to the MCP database tools. |
| `RESERVATIONS_API_KEY` | `restaurant_concierge/reservations.py` | Authorization for retrieving the reservations list will fail. |

## Known Constraints

- Requires active GCP billing and permissions.
- Local execution of seeding/agent scripts requires GCP credentials (ADC) or environment setup.
- The `cloud-sql-python-connector` is used for connecting to PostgreSQL without requiring the Cloud SQL Auth Proxy.

<!-- MANUAL ADDITIONS START -->
<!-- Add any manual context below this line -->
<!-- MANUAL ADDITIONS END -->
