# Research: Table Reservation System

## Decisions

### 1. Concurrency Control (Double-Booking Prevention)

- **Decision**: Use explicit row locking via `SELECT ... FOR UPDATE` (or database transactions with suitable locking) during capacity checks. When checking the capacity for a given time slot, we query:
  `SELECT SUM(party_size) FROM reservations WHERE date = :date AND time = :time FOR UPDATE`
- **Rationale**: Ensures that concurrent requests trying to write to the same time slot will serialize, preventing double-bookings and maintaining strict consistency under peak load.
- **Alternatives considered**:
  - *Optimistic Concurrency Control (OCC)*: Rejected because it requires adding version fields to models and handling retries at the application layer, which adds complexity.
  - *In-Memory Locking (e.g. asyncio locks)*: Rejected because it does not scale across multiple process instances (e.g., if Uvicorn runs multiple workers or instances).

### 2. API Key Authentication

- **Decision**: Authenticate `GET /reservations` using a header-based API key lookup (specifically looking for an `X-API-KEY` header). The API key value will be read from the environment (`RESERVATIONS_API_KEY`).
- **Rationale**: Straightforward to implement using FastAPI's `Security` and `APIKeyHeader` dependencies. It meets the "simple pre-shared token/API key" requirement without the overhead of OAuth2 or session state management.
- **Alternatives considered**:
  - *OAuth2 with JWTs*: Rejected as it introduces unnecessary complexity (user auth, token sign/verify) for a single-role internal endpoint.
  - *Query Parameter API Key*: Rejected because headers are generally preferred for API keys to avoid exposing sensitive tokens in URL logs.

### 3. Database Driver & Connection

- **Decision**: Use `SQLAlchemy` (sync/async) with `pg8000` driver to connect via the `cloud-sql-python-connector`.
- **Rationale**: Since `cloud-sql-python-connector[pg8000]` is already an established dependency in the repository, using it with SQLAlchemy is the most direct and consistent path.
- **Alternatives considered**:
  - *psycopg2*: Rejected because `pg8000` is already configured and validated in the stack.
