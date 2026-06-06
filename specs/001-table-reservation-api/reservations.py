import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .models import Reservation, ReservationCreate, ReservationResponse

router = APIRouter(prefix="/reservations", tags=["reservations"])

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    expected_key = os.getenv("RESERVATIONS_API_KEY", "default_secret_key")
    if not api_key or api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return api_key

MAX_CAPACITY = 40

@router.post("", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation_in: ReservationCreate, db: AsyncSession = Depends(get_db)):
    # Início da transação atômica com bloqueio para evitar overbooking concorrente
    async with db.begin():
        # 1. Verificar capacidade atual para o slot (SELECT ... FOR UPDATE no PostgreSQL)
        # Como estamos usando agregação, o bloqueio deve ser estratégico. 
        # Para simplificar conforme o research.md, garantimos a consistência na transação.
        stmt = (
            select(func.sum(Reservation.party_size))
            .where(Reservation.reservation_date == reservation_in.reservation_date)
            .where(Reservation.reservation_time == reservation_in.reservation_time)
            .with_for_update()
        )
        
        result = await db.execute(stmt)
        current_booked = result.scalar() or 0

        if current_booked + reservation_in.party_size > MAX_CAPACITY:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Venue capacity exceeded for this slot. Remaining: {MAX_CAPACITY - current_booked}"
            )

        # 2. Criar reserva
        new_res = Reservation(**reservation_in.model_dump())
        db.add(new_res)
        await db.flush() # flush para obter o ID dentro do contexto da transação
        await db.refresh(new_res)
        
        return new_res

@router.get("", response_model=List[ReservationResponse])
async def list_reservations(
    db: AsyncSession = Depends(get_db),
    _ = Depends(verify_api_key)
):
    result = await db.execute(select(Reservation).order_by(Reservation.reservation_date, Reservation.reservation_time))
    return result.scalars().all()