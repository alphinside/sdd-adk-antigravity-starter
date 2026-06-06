# Quickstart: Table Reservation System

## Setup Environment

Ensure you have configured your environment variables in `.env`:
```bash
RESERVATIONS_API_KEY=your_secret_api_key_here
```

## Running Tests

To execute the suite of pytest tests (including behavior-driven tests validating validations, capacity checks, double-booking prevention, and list retrieval):
```bash
uv run pytest tests/
```

## Running the Application Locally

1. Ensure the PostgreSQL database is running and setup scripts are applied.
2. Start the FastAPI development server:
   ```bash
   uv run python server.py
   ```
3. Interactive API documentation is available at [http://localhost:8080/docs](http://localhost:8080/docs).
4. Send a test POST request to reserve a table:
   ```bash
   curl -X POST http://localhost:8080/reservations \
     -H "Content-Type: application/json" \
     -d '{"customer_name": "Alice", "email": "alice@example.com", "phone": "+1234567890", "party_size": 4, "reservation_date": "2026-06-15", "reservation_time": "19:00:00"}'
   ```
5. Fetch existing reservations (requires the pre-shared key header):
   ```bash
   curl -H "X-API-KEY: your_secret_api_key_here" http://localhost:8080/reservations
   ```
