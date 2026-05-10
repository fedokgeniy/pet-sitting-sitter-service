from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class SitterCreate(BaseModel):
    sitter_id: str
    user_id: str
    full_name: str
    photo_url: str | None = None
    description: str | None = None
    hourly_rate: Decimal
    max_radius_km: int | None = None


class SitterOut(SitterCreate):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ServiceTypeOut(BaseModel):
    service_type_id: str
    code: str
    name: str
    description: str | None = None
    duration_minutes: int | None = None
    base_price: Decimal | None = None

    class Config:
        from_attributes = True


class CalendarSlotOut(BaseModel):
    slot_id: str
    sitter_id: str
    start_at: datetime
    end_at: datetime
    status: str
    capacity: int
    created_at: datetime

    class Config:
        from_attributes = True
