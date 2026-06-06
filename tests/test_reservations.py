import os
import pytest
from httpx import AsyncClient
from datetime import date, time, timedelta

@pytest.mark.anyio
async def test_create_valid_reservation(async_client: AsyncClient):
    future_date = (date.today() + timedelta(days=5)).isoformat()
    payload = {
        "customer_name": "Alice",
        "email": "alice@example.com",
        "phone": "+1234567890",
        "party_size": 4,
        "reservation_date": future_date,
        "reservation_time": "19:00:00"
    }
    response = await async_client.post("/reservations", json=payload)
    assert response.status_code == 201
    assert response.json()["customer_name"] == "Alice"
    assert "id" in response.json()

@pytest.mark.anyio
async def test_reject_past_date(async_client: AsyncClient):
    payload = {
        "customer_name": "Bob",
        "email": "bob@example.com",
        "phone": "555-5555",
        "party_size": 2,
        "reservation_date": "2020-01-01",
        "reservation_time": "12:00:00"
    }
    response = await async_client.post("/reservations", json=payload)
    assert response.status_code == 422 # Pydantic validation error

@pytest.mark.anyio
async def test_overbooking_prevention(async_client: AsyncClient):
    future_date = (date.today() + timedelta(days=10)).isoformat()
    # Fill capacity (40 seats)
    resp1 = await async_client.post("/reservations", json={
        "customer_name": "Full House", "email": "f@test.com", "phone": "12345",
        "party_size": 20, "reservation_date": future_date, "reservation_time": "20:00:00"
    })
    assert resp1.status_code == 201
    
    resp2 = await async_client.post("/reservations", json={
        "customer_name": "Full House 2", "email": "f2@test.com", "phone": "12345",
        "party_size": 20, "reservation_date": future_date, "reservation_time": "20:00:00"
    })
    assert resp2.status_code == 201
    
    # Attempt to book 1 more seat
    response = await async_client.post("/reservations", json={
        "customer_name": "Extra Guest", "email": "extra@test.com", "phone": "12345",
        "party_size": 1, "reservation_date": future_date, "reservation_time": "20:00:00"
    })
    assert response.status_code == 400
    assert "Venue capacity exceeded" in response.json()["detail"]

@pytest.mark.anyio
async def test_list_reservations_auth(async_client: AsyncClient):
    # 1. No key
    resp_no_key = await async_client.get("/reservations")
    assert resp_no_key.status_code == 401

    # 2. Wrong key
    resp_wrong = await async_client.get("/reservations", headers={"X-API-KEY": "wrong"})
    assert resp_wrong.status_code == 401

    # 3. Correct key
    resp_correct = await async_client.get("/reservations", headers={"X-API-KEY": "secret123"})
    assert resp_correct.status_code == 200
    assert isinstance(resp_correct.json(), list)
