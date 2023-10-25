from numbers import Number
from typing import Any, Dict, Literal

from models.product import TypeEnum


class ProductValidator:
    """A class for validating product data."""

    @staticmethod
    def validate(**kwargs: Dict[str, Any]) -> dict | Literal[True]:
        """
        Validates the given product data.

        Args:
            **kwargs (Dict[str, Any]): The product data to be validated.

        Returns:
            bool: True if the product data is valid, False otherwise.
        """
        errors = {}

        required_fields = ["name", "price", "type"]
        for field in required_fields:
            if not kwargs.get(field):
                errors[field] = f"{field.capitalize()} is required"

        if not isinstance(kwargs.get("price"), Number):
            errors["price"] = "Price must be a number"

        # if kwargs.get("type") not in [item.value for item in TypeEnum]:
        #     errors["type"] = "Type must be one of the following: appetizer, dish, dessert, drink"

        return errors if errors else True
