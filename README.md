# Restaurant Concierge — SDD with ADK & Antigravity

This is the companion repository for the **"Spec-Driven AI Agent Development with Antigravity"** codelab.

## What's in this repo

A restaurant concierge starter application powered by a Google ADK agent. The starter code provides:

- A working ADK agent with menu search (keyword + RAG-powered semantic search via MCP Toolbox) and dietary preference tracking (via ToolContext)
- SDD workflows (`.agents/workflows/`) for the specify → plan → tasks → implement cycle
- A pre-configured Antigravity skill with ADK codelab reference patterns and repo research
- Database scripts for Cloud SQL setup, seeding, and embedding generation
- **Table Reservation API (`001-table-reservation-api`)**: Fully implemented production backend supporting table reservations (`POST /reservations`), capacity limits (`MAX_CAPACITY = 40`), concurrency protection, and secured reservation listings (`GET /reservations`).

## Codelab

Follow the step-by-step tutorial to extend this starter code using Spec-Driven Development with Antigravity:

**[Spec-Driven AI Agent Development with Antigravity](#)** *(link to published codelab)*

## Local Configuration & Runbook

### 1. Environment Configuration

Create or update your `.env` file with the following variables:

```bash
DATABASE_URL=sqlite+aiosqlite:///:memory:
RESERVATIONS_API_KEY=secret123
PORT=8080
```

### 2. Running Tests (100% Test Coverage via AnyIO & Pytest)

To execute the automated BDD and security test suite validating input rules, past dates rejection, overbooking prevention (40 seats max), and API Key header authentication:

```bash
uv run pytest tests/
```

### 3. Running the Server Locally

Start the live dev server (with hot reload or standalone Uvicorn):

```bash
uv run python server.py
```

### 4. Interactive API Documentation & Verification

- OpenAPI interactive UI: [http://localhost:8080/docs](http://localhost:8080/docs)
- **Reserve a Table (`POST /reservations`)**:
  ```bash
  curl -X POST http://localhost:8080/reservations \
    -H "Content-Type: application/json" \
    -d '{"customer_name": "Alice", "email": "alice@example.com", "phone": "+1234567890", "party_size": 4, "reservation_date": "2026-06-15", "reservation_time": "19:00:00"}'
  ```
- **List Reservations (`GET /reservations` secured via header)**:
  ```bash
  curl -H "X-API-KEY: secret123" http://localhost:8080/reservations
  ```

## Prerequisites

- [Google Antigravity](https://antigravity.google) and git
- A Google Cloud account with trial billing
- Run `bash scripts/setup_prerequisites.sh` to install all other required tools

## Quick start

```bash
git clone https://github.com/alphinside/sdd-adk-antigravity-starter.git sdd-adk-agents-agy
cd sdd-adk-agents-agy
bash scripts/setup_prerequisites.sh
```

Then follow the codelab instructions.
