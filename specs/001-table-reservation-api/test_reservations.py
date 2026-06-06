import pytest
from httpx import AsyncClient, ASGITransport
from server import app
from datetime import date, time, timedelta
import os

@pytest.mark.asyncio
async def test_create_valid_reservation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        future_date = (date.today() + timedelta(days=5)).isoformat()
        payload = {
            "customer_name": "Alice",
            "email": "alice@example.com",
            "phone": "+1234567890",
            "party_size": 4,
            "reservation_date": future_date,
            "reservation_time": "19:00:00"
        }
        response = await ac.post("/reservations", json=payload)
    assert response.status_code == 201
    assert response.json()["customer_name"] == "Alice"
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_reject_past_date():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "customer_name": "Bob",
            "email": "bob@example.com",
            "phone": "555-5555",
            "party_size": 2,
            "reservation_date": "2020-01-01",
            "reservation_time": "12:00:00"
        }
        response = await ac.post("/reservations", json=payload)
    assert response.status_code == 422 # Pydantic validation error

@pytest.mark.asyncio
async def test_overbooking_prevention():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        future_date = (date.today() + timedelta(days=10)).isoformat()
        # Fill capacity (40 seats)
        await ac.post("/reservations", json={
            "customer_name": "Full House", "email": "f@test.com", "phone": "123",
            "party_size": 20, "reservation_date": future_date, "reservation_time": "20:00:00"
        })
        await ac.post("/reservations", json={
            "customer_name": "Full House 2", "email": "f2@test.com", "phone": "123",
            "party_size": 20, "reservation_date": future_date, "reservation_time": "20:00:00"
        })
        
        # Attempt to book 1 more seat
        response = await ac.post("/reservations", json={
            "customer_name": "Extra Guest", "email": "extra@test.com", "phone": "123",
            "party_size": 1, "reservation_date": future_date, "reservation_time": "20:00:00"
        })
    assert response.status_code == 400
    assert "capacity exceeded" in response.json()["detail"]

@pytest.mark.asyncio
async def test_list_reservations_auth():
    os.environ["RESERVATIONS_API_KEY"] = "secret123"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. No key
        resp_no_key = await ac.get("/reservations")
        assert resp_no_key.status_code == 401

        # 2. Wrong key
        resp_wrong = await ac.get("/reservations", headers={"X-API-KEY": "wrong"})
        assert resp_wrong.status_code == 401

        # 3. Correct key
        resp_correct = await ac.get("/reservations", headers={"X-API-KEY": "secret123"})
        assert resp_correct.status_code == 200
        assert isinstance(resp_correct.json(), list)