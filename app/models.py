from sqlalchemy import Column, String, Text, DateTime, Numeric, Integer, Boolean, ForeignKey

from .database import Base


class SitterProfile(Base):
    __tablename__ = "sitter_profiles"
    __table_args__ = {"schema": "sitter"}

    sitter_id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, unique=True)
    full_name = Column(String(200), nullable=False)
    photo_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    max_radius_km = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class ServiceType(Base):
    __tablename__ = "service_types"
    __table_args__ = {"schema": "sitter"}

    service_type_id = Column(String(36), primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    base_price = Column(Numeric(10, 2), nullable=True)


class SitterService(Base):
    __tablename__ = "sitter_services"
    __table_args__ = {"schema": "sitter"}

    sitter_service_id = Column(String(36), primary_key=True)
    sitter_id = Column(String(36), ForeignKey("sitter.sitter_profiles.sitter_id"), nullable=False)
    service_type_id = Column(String(36), ForeignKey("sitter.service_types.service_type_id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    max_pets = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)


class SitterSkill(Base):
    __tablename__ = "sitter_skills"
    __table_args__ = {"schema": "sitter"}

    sitter_skill_id = Column(String(36), primary_key=True)
    sitter_id = Column(String(36), ForeignKey("sitter.sitter_profiles.sitter_id"), nullable=False)
    skill_code = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)


class SitterCalendarSlot(Base):
    __tablename__ = "sitter_calendar_slots"
    __table_args__ = {"schema": "sitter"}

    slot_id = Column(String(36), primary_key=True)
    sitter_id = Column(String(36), ForeignKey("sitter.sitter_profiles.sitter_id"), nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    status = Column(String(32), nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)


class SitterCapacityLimit(Base):
    __tablename__ = "sitter_capacity_limits"
    __table_args__ = {"schema": "sitter"}

    limit_id = Column(String(36), primary_key=True)
    sitter_id = Column(String(36), ForeignKey("sitter.sitter_profiles.sitter_id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    max_bookings_per_day = Column(Integer, nullable=False)
    max_hours_per_day = Column(Integer, nullable=False)
