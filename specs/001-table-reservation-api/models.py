from datetime import date, time, datetime
from typing import Annotated
from sqlalchemy import Column, Integer, String, Date, Time, DateTime, func
from pydantic import BaseModel, EmailStr, Field, field_validator
from .database import Base

# --- SQLAlchemy Model ---
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    party_size = Column(Integer, nullable=False)
    reservation_date = Column(Date, nullable=False)
    reservation_time = Column(Time, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

# --- Pydantic Schemas ---
class ReservationBase(BaseModel):
    customer_name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., min_length=5)
    party_size: int = Field(..., ge=1, le=20)
    reservation_date: date
    reservation_time: time

    @field_validator("reservation_date")
    @classmethod
    def date_must_be_future(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Reservation date must be in the future")
        return v

class ReservationCreate(ReservationBase):
    @field_validator("reservation_time")
    @classmethod
    def time_must_be_future_if_today(cls, v: time, info) -> time:
        if "reservation_date" in info.data and info.data["reservation_date"] == date.today():
            if v < datetime.now().time():
                raise ValueError("Reservation time must be in the future for today's bookings")
        return v

class ReservationResponse(ReservationBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}