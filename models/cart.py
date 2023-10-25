from typing import List, Tuple, Union
from uuid import uuid4

from app import db
from models import BaseModel
from models.order import Order


cartOrder = db.Table(
    "cartOrder",
    db.Column("cartId", db.Integer, db.ForeignKey("cart.id")),
    db.Column("orderId", db.Integer, db.ForeignKey("order.id")),
)


class Cart(BaseModel):
    __tablename__ = "cart"

    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    orders = db.relationship(Order, secondary=cartOrder, backref="cart")

    def __repr__(self) -> str:
        return "<Cart '{}'>".format(self.user.email)
