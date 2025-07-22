"""
General business-logic layer.
"""

from typing import List, Any, TypeVar, Generic, Type
from sqlalchemy.orm import Session

from app.data_access_layer.database import Base
from app.data_access_layer.general_repository import GeneralRepository
from app.exceptions import NotFoundError


Item = TypeVar("Item", bound=Base)


class GeneralService(Generic[Item]):
    """
    General service class that orchestrates business logic and use cases for a given SQLAlchemy model.
    Provides methods for listing, retrieving, creating, updating, and deleting model instances.
    """

    def __init__(self, db: Session, model=Type[Item]):
        self.repo = GeneralRepository(db=db, model=model)
        self.model = model

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Item]:
        return self.repo.list(skip=skip, limit=limit)

    def get(self, item_id: int) -> Item:
        item = self.repo.get(item_id)
        if not item:
            raise NotFoundError(f"Item with id {item_id} not found")
        return item

    def get_by_attributes(
        self,
        attributes: dict[str, Any],
        limit: int = 10,
        order_by: str | None = None,
        descending: bool = False,
    ) -> List[Item]:
        if order_by:
            try:
                order_by = getattr(self.model, order_by)
            except AttributeError:
                raise ValueError(f"Item does not have attribute: {order_by}")
            order_by = order_by.desc() if descending else order_by.asc()
        items = self.repo.find_by(limit=limit, order_by=order_by, **attributes)
        if not items:
            raise NotFoundError(f"Items with attributes {attributes} not found")
        return items

    def create(self, item_data: dict[str, Any]) -> Item:
        return self.repo.add(**item_data)

    def update(self, item_id: int, data: dict[str, Any]) -> Item:
        updated = self.repo.update(item_id, data)
        if not updated:
            raise NotFoundError(f"Item {item_id} not found")
        return updated

    def delete(self, item_id: int) -> Item:
        deleted = self.repo.delete(item_id)
        if not deleted:
            raise NotFoundError(f"Item {item_id} not found")
        return deleted
