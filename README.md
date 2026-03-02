# Restaurant Concierge — SDD with ADK & Antigravity

This is the companion repository for the **"Spec-Driven AI Agent Development with Antigravity"** codelab.

## What's in this repo

A restaurant concierge starter application powered by a Google ADK agent. The starter code provides:

- A working ADK agent with menu search (keyword + RAG-powered semantic search via MCP Toolbox) and dietary preference tracking (via ToolContext)
- SDD workflows (`.agents/workflows/`) for the specify → plan → tasks → implement cycle
- A pre-configured Antigravity skill with ADK codelab reference patterns and repo research
- Database scripts for Cloud SQL setup, seeding, and embedding generation

## Codelab

Follow the step-by-step tutorial to extend this starter code using Spec-Driven Development with Antigravity:

**[Spec-Driven AI Agent Development with Antigravity](#)** *(link to published codelab)*

## What you'll build

Using Antigravity's SDD workflows, you the following feature to the existing agent:

1. **Reservation Booking** — Add reservation management tools (create + list) via MCP Toolbox, backed by a new Cloud SQL table

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
