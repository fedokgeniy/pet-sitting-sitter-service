from decimal import Decimal

from app.schemas import SitterCreate, ServiceTypeOut


def test_sitter_create_minimal_fields():
    payload = SitterCreate(
        sitter_id="s1",
        user_id="u1",
        full_name="John",
        hourly_rate=Decimal("15.00"),
    )
    assert payload.sitter_id == "s1"
    assert payload.photo_url is None
    assert payload.hourly_rate == Decimal("15.00")


def test_sitter_create_full_fields():
    payload = SitterCreate(
        sitter_id="s2",
        user_id="u2",
        full_name="Mary",
        photo_url="https://example.com/p.jpg",
        description="cats",
        hourly_rate=Decimal("18.5"),
        max_radius_km=15,
    )
    assert payload.max_radius_km == 15
    assert payload.description == "cats"


def test_service_type_out_optional():
    s = ServiceTypeOut(service_type_id="t1", code="walk", name="Dog Walk")
    assert s.duration_minutes is None
    assert s.base_price is None
