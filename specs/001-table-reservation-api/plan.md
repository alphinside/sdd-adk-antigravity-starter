# Implementation Plan: Table Reservation System

**Branch**: `001-table-reservation-api` | **Date**: 2026-06-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-table-reservation-api/spec.md`

## Summary

Build a backend API with FastAPI for a table reservation system. The system will support creating reservations (`POST /reservations`) and listing reservations (`GET /reservations`). The data will be stored in PostgreSQL, and the listing endpoint will be secured using a simple pre-shared API key token. Venue capacity is checked against a static total seat count (40 seats) to prevent overbooking.

## Technical Context

**Language/Version**: Python `>=3.12`  
**Primary Dependencies**: FastAPI, SQLAlchemy, pytest, pytest-asyncio, psycopg2-binary or pg8000  
**Storage**: PostgreSQL (Cloud SQL)  
**Testing**: pytest with pytest-asyncio  
**Target Platform**: Linux server  
**Performance Goals**: `<200ms` response times for reservation creation, `<100ms` for listings  
**Constraints**: Static capacity limit (40 seats), Simple API key authentication for GET requests  
**Scale/Scope**: Relational storage for reservations, concurrent booking protection using database transactions / locking  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Unified Tech Stack**: Does this service use FastAPI for web services and Cloud SQL (PostgreSQL) for the database?
- [x] **Shift-Left Testing**: Are tests written using pytest *before* implementation for all new endpoints?
- [x] **BDD Specifications**: Does the feature specification follow Behavior-Driven Development (BDD) principles (Given/When/Then)?

## Project Structure

### Documentation (this feature)

```text
specs/001-table-reservation-api/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── openapi.json     # OpenAPI contract for the endpoints
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
restaurant_concierge/
├── __init__.py
├── agent.py
├── database.py           # Database connection and setup
├── models.py             # SQLAlchemy models and Pydantic schemas
└── reservations.py       # FastAPI router for reservations

tests/
├── conftest.py          # Pytest fixtures and DB setup
└── test_reservations.py  # Behavior-driven pytest tests

server.py                 # Main server entrypoint wrapping both agent & reservations
```

**Structure Decision**: Option 1 (Single project), extending the current `restaurant_concierge` module.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*(No violations. The stack perfectly adheres to FastAPI, PostgreSQL, and pytest.)*
