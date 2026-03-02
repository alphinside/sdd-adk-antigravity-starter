# Restaurant Concierge — SDD with ADK & Antigravity

This is the companion repository for the **"Spec-Driven AI Agent Development with Antigravity"** codelab.

## What's in this repo

A restaurant concierge starter application powered by a Google ADK agent. The starter code provides:

- A working ADK agent with menu search (keyword + RAG-powered semantic search via MCP Toolbox) and dietary preference tracking (via ToolContext)
- SDD workflows (`.agents/workflows/`) for the specify → plan → tasks → implement cycle
- A pre-configured Antigravity skill with ADK codelab reference patterns (`.agents/skills/adk-codelab-patterns/`)
- Database scripts for Cloud SQL setup, seeding, and embedding generation

## Codelab

Follow the step-by-step tutorial to extend this starter code using Spec-Driven Development with Antigravity:

**[Spec-Driven AI Agent Development with Antigravity](#)** *(link to published codelab)*

## What you'll build

Using Antigravity's SDD workflows, you add two features to the existing agent:

1. **Reservation Booking** — Add reservation management tools (create + list) via MCP Toolbox, backed by a new Cloud SQL table
2. **Web Chat Interface** — A vanilla HTML/CSS/JS chat widget with a floating button, real-time SSE streaming from ADK's `/run_sse` endpoint, and session management

## Prerequisites

- [Google Antigravity](https://antigravity.google)
- A Google Cloud account with trial billing
- Completion of the four prerequisite ADK codelabs (or equivalent knowledge)
- Run `bash scripts/setup_prerequisites.sh` to install all other required tools

## Quick start

```bash
git clone https://github.com/alphinside/sdd-adk-agents-agy.git
cd sdd-adk-agents-agy
bash scripts/setup_prerequisites.sh
```

Then follow the codelab instructions.
