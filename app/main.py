from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .init_db import create_schema_and_tables, seed_stub_data
from .logging_config import configure_logging, get_logger
from .models import SitterProfile, ServiceType, SitterCalendarSlot
from .schemas import SitterCreate, SitterOut, ServiceTypeOut, CalendarSlotOut

configure_logging()
logger = get_logger(__name__)

app = FastAPI(title="Sitter Service")


@app.on_event("startup")
def startup() -> None:
    logger.info("Sitter service is starting up")
    create_schema_and_tables()
    logger.info("Sitter service startup completed")


@app.get("/health")
def health():
    logger.debug("Health check requested")
    return {"service": "sitter_service", "status": "ok"}


@app.post("/init-db")
def init_db():
    logger.info("Manual /init-db invoked")
    create_schema_and_tables()
    return {"status": "ok", "schema": "sitter"}


@app.post("/seed")
def seed():
    logger.info("Manual /seed invoked")
    seed_stub_data()
    return {"status": "ok", "schema": "sitter", "message": "stub data inserted"}


@app.get("/sitters", response_model=list[SitterOut])
def get_sitters(db: Session = Depends(get_db)):
    logger.info("GET /sitters")
    return db.query(SitterProfile).order_by(SitterProfile.created_at.desc()).all()


@app.get("/sitters/{sitter_id}", response_model=SitterOut)
def get_sitter(sitter_id: str, db: Session = Depends(get_db)):
    logger.info("GET /sitters/%s", sitter_id)
    item = db.query(SitterProfile).filter(SitterProfile.sitter_id == sitter_id).first()
    if not item:
        logger.warning("Sitter not found: %s", sitter_id)
        raise HTTPException(status_code=404, detail="Sitter not found")
    return item


@app.post("/sitters", response_model=SitterOut)
def create_sitter(payload: SitterCreate, db: Session = Depends(get_db)):
    logger.info("POST /sitters sitter_id=%s", payload.sitter_id)
    try:
        item = SitterProfile(
            sitter_id=payload.sitter_id,
            user_id=payload.user_id,
            full_name=payload.full_name,
            photo_url=payload.photo_url,
            description=payload.description,
            hourly_rate=payload.hourly_rate,
            max_radius_km=payload.max_radius_km,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        logger.info("Sitter created: %s", item.sitter_id)
        return item
    except Exception as ex:
        logger.exception("Failed to create sitter: %s", ex)
        raise HTTPException(status_code=500, detail=str(ex))


@app.get("/services", response_model=list[ServiceTypeOut])
def get_services(db: Session = Depends(get_db)):
    logger.info("GET /services")
    return db.query(ServiceType).order_by(ServiceType.name.asc()).all()


@app.get("/calendar-slots", response_model=list[CalendarSlotOut])
def get_calendar_slots(db: Session = Depends(get_db)):
    logger.info("GET /calendar-slots")
    return db.query(SitterCalendarSlot).order_by(SitterCalendarSlot.start_at.asc()).all()
