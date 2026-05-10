from datetime import datetime

from sqlalchemy.orm import Session

from .database import Base, engine, ensure_schema
from .logging_config import get_logger
from .models import (
    SitterProfile,
    ServiceType,
    SitterService,
    SitterSkill,
    SitterCalendarSlot,
    SitterCapacityLimit,
)

logger = get_logger(__name__)


def create_schema_and_tables() -> None:
    logger.info("Creating schema 'sitter' and its tables")
    ensure_schema("sitter")
    Base.metadata.create_all(
        bind=engine,
        tables=[
            SitterProfile.__table__,
            ServiceType.__table__,
            SitterService.__table__,
            SitterSkill.__table__,
            SitterCalendarSlot.__table__,
            SitterCapacityLimit.__table__,
        ],
    )
    logger.info("Schema 'sitter' is ready")


def seed_stub_data() -> None:
    logger.info("Seeding stub data for sitter service")
    with Session(engine) as session:
        if session.query(SitterProfile).first():
            logger.info("Stub data already present, skip seeding")
            return

        sitter1 = SitterProfile(
            sitter_id="11111111-1111-1111-1111-111111111111",
            user_id="21111111-1111-1111-1111-111111111111",
            full_name="John Doe",
            photo_url="https://example.com/john.jpg",
            description="Experienced dog sitter",
            hourly_rate=15.00,
            max_radius_km=10,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        sitter2 = SitterProfile(
            sitter_id="22222222-2222-2222-2222-222222222222",
            user_id="22222222-1111-1111-1111-111111111111",
            full_name="Mary Paws",
            photo_url="https://example.com/mary.jpg",
            description="Cat care specialist",
            hourly_rate=18.00,
            max_radius_km=15,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        walk = ServiceType(
            service_type_id="33333333-3333-3333-3333-333333333331",
            code="walk",
            name="Dog Walk",
            description="One hour walking service",
            duration_minutes=60,
            base_price=10.00,
        )
        daycare = ServiceType(
            service_type_id="33333333-3333-3333-3333-333333333332",
            code="daycare",
            name="Day Care",
            description="Day care service",
            duration_minutes=480,
            base_price=40.00,
        )

        session.add_all([sitter1, sitter2, walk, daycare])
        session.flush()

        session.add_all([
            SitterService(
                sitter_service_id="44444444-4444-4444-4444-444444444441",
                sitter_id=sitter1.sitter_id,
                service_type_id=walk.service_type_id,
                price=12.00,
                max_pets=2,
                is_active=True,
            ),
            SitterService(
                sitter_service_id="44444444-4444-4444-4444-444444444442",
                sitter_id=sitter2.sitter_id,
                service_type_id=daycare.service_type_id,
                price=45.00,
                max_pets=1,
                is_active=True,
            ),
            SitterSkill(
                sitter_skill_id="55555555-5555-5555-5555-555555555551",
                sitter_id=sitter1.sitter_id,
                skill_code="dogs_large",
                description="Can handle large dogs",
            ),
            SitterSkill(
                sitter_skill_id="55555555-5555-5555-5555-555555555552",
                sitter_id=sitter2.sitter_id,
                skill_code="cats_meds",
                description="Can administer cat medication",
            ),
            SitterCalendarSlot(
                slot_id="66666666-6666-6666-6666-666666666661",
                sitter_id=sitter1.sitter_id,
                start_at=datetime(2026, 5, 1, 9, 0, 0),
                end_at=datetime(2026, 5, 1, 10, 0, 0),
                status="free",
                capacity=1,
                created_at=datetime.utcnow(),
            ),
            SitterCalendarSlot(
                slot_id="66666666-6666-6666-6666-666666666662",
                sitter_id=sitter2.sitter_id,
                start_at=datetime(2026, 5, 1, 10, 0, 0),
                end_at=datetime(2026, 5, 1, 18, 0, 0),
                status="free",
                capacity=1,
                created_at=datetime.utcnow(),
            ),
            SitterCapacityLimit(
                limit_id="77777777-7777-7777-7777-777777777771",
                sitter_id=sitter1.sitter_id,
                day_of_week=1,
                max_bookings_per_day=4,
                max_hours_per_day=8,
            ),
            SitterCapacityLimit(
                limit_id="77777777-7777-7777-7777-777777777772",
                sitter_id=sitter2.sitter_id,
                day_of_week=2,
                max_bookings_per_day=3,
                max_hours_per_day=6,
            ),
        ])

        session.commit()
        logger.info("Stub data seeded successfully")
