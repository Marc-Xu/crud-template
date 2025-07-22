import pytest

from app.exceptions import NotFoundError, ValidationError
from app.business_logic.restaurant_service import RestaurantService


@pytest.fixture
def service(db_session):
    return RestaurantService(db=db_session)


def test_create_and_unique(service):
    data = {"name": "Test", "cuisine": "C", "rating": 4.4}
    r1 = service.create(data)
    assert r1.name == "Test"
    # duplicate name business rule
    with pytest.raises(ValidationError) as exc:
        service.create(data)
    assert "already exists" in str(exc.value)


def test_get_not_found(service):
    with pytest.raises(NotFoundError):
        service.get(9999)


def test_get_restaurant_by_attributes(service):
    data1 = {"name": "R1", "cuisine": "special", "rating": 4.5}
    data2 = {"name": "R2", "cuisine": "special", "rating": 4.3}
    service.create(data1)
    service.create(data2)
    top = service.get_by_attributes(
        {"cuisine": "special"}, limit=2, order_by="rating", descending=True
    )
    assert top is not None and len(top) == 2
    assert top[0].name == "R1"
    assert top[1].name == "R2"


def test_update_and_not_found(service):
    data = {"name": "Up", "cuisine": None, "rating": 1.0}
    r = service.create(data)
    update_data = {"rating": 2.0}
    r2 = service.update(r.id, update_data)
    assert abs(r2.rating - 2.0) < 1e-6
    with pytest.raises(NotFoundError):
        service.update(9999, update_data)


def test_delete_and_not_found(service):
    data = {"name": "Del", "cuisine": None, "rating": 3.3}
    r = service.create(data)
    d = service.delete(r.id)
    assert d.id == r.id
    with pytest.raises(NotFoundError):
        service.delete(9999)
