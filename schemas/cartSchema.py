from flask_restx import Namespace, fields

from schemas.orderSchema import OrderSchema
from schemas.userSchema import UserSchema


class CartSchema:
    api = Namespace("Cart", description="Cart related operations")

    cart = api.model(
        "cart",
        {
            "publicId": fields.String(description="cart Identifier"),
            "user": fields.Nested(UserSchema.user),
            "orders": fields.List(fields.Nested(OrderSchema.order)),
        },
    )
