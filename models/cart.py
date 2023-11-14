from config.app import db
from models import BaseModel

cartOrder = db.Table(
    "cartOrder",
    db.Column("cartId", db.Integer, db.ForeignKey("cart.id")),
    db.Column("orderId", db.Integer, db.ForeignKey("order.id")),
)


class Cart(BaseModel):
    __tablename__ = "cart"

    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="cart", lazy="joined", uselist=False)
    orders = db.relationship(
        "Order",
        secondary=cartOrder,
        backref="cart",
        lazy="joined",
        uselist=True,
        cascade="all, delete",
    )

    def __repr__(self) -> str:
        return f"<Cart '{self.user.email}'>"
