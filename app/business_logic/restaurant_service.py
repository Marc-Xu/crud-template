"""
Business-logic layer orchestrating restaurant use-cases.
"""

from typing import Any

from app.business_logic.general_service import GeneralService
from app.data_access_layer.models import Restaurant
from app.exceptions import ValidationError


class RestaurantService(GeneralService[Restaurant]):
    """
    Orchestrates business rules and use-cases for Restaurant.
    """

    def create(self, restaurant_data: dict[str, Any]) -> Restaurant:
        # Example Business rule: name must be unique
        if self.repo.find_by(name=restaurant_data["name"]):
            raise ValidationError(
                f"A restaurant named '{restaurant_data["name"]}' already exists"
            )
        return self.repo.add(**restaurant_data)
