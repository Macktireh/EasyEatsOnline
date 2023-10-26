from flask_restx import Namespace, fields
from schemas.productSchema import ProductSchema

from schemas.userSchema import UserSchema


class OrderSchema:
    api = Namespace("Oerder", description="Order related operations")

    order = api.model(
        "order",
        {
            "publicId": fields.String(description="order Identifier"),
            "user": fields.Nested(UserSchema.user),
            "product": fields.List(fields.Nested(ProductSchema.product)),
            "quantity": fields.Integer(required=True, description="order quantity"),
            "ordered": fields.Boolean(required=True, description="order ordered"),
            "orderDate": fields.DateTime(required=True, description="order date"),
            "createdAt": fields.DateTime(readonly=True, description="order created at"),
        },
    )

    updateQuantityOrder = api.model(
        "updateQuantityOrder",
        {
            "publicId": fields.String(required=True, description="order Identifier"),
            "quantity": fields.Integer(required=True, description="order quantity", min=1, max=20),
        },
    )
