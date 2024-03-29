from numbers import Number
from typing import Any, Dict, Literal


class OrderValidator:
    """A class for validating order data."""

    @staticmethod
    def validate(**kwargs: Dict[str, Any]) -> dict | Literal[True]:
        """
        Validates the given order data.

        Args:
            **kwargs (Dict[str, Any]): The order data to be validated.

        Returns:
            bool: True if the order data is valid, False otherwise.
        """
        errors = {}

        required_fields = ["quantity"]
        for field in required_fields:
            if not kwargs.get(field):
                errors[field] = f"{field.capitalize()} is required"

        if not isinstance(kwargs.get("quantity"), Number):
            errors["quantity"] = "Quantity must be a number"
        elif kwargs.get("quantity") < 1 or kwargs.get("quantity") > 20:
            errors["quantity"] = "Quantity must be between 1 and 20"

        return errors if errors else True
