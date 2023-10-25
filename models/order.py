from app import db
from models import BaseModel


class Order(BaseModel):
    __tablename__ = "order"

    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    productId = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    ordered = db.Column(db.Boolean, nullable=False, default=False)
    orderDate = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return "<Order '{} ({})'>".format(self.product.name, self.quantity)
