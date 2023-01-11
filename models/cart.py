from typing import List, Tuple, Union
from uuid import uuid4

from app import db
from models.order import Order


cartOrder = db.Table('cartOrder', db.Column('cartId', db.Integer, db.ForeignKey('cart.id')), db.Column('orderId', db.Integer, db.ForeignKey('order.id')))


class Cart(db.Model):
    
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.Text, unique=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    orders = db.relationship(Order, secondary=cartOrder, backref='cart')
    
    def save(self) -> "Cart":
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def create(cls, userId: int) -> "Cart":
        category = cls(publicId=str(uuid4()), userId=userId)
        return category.save()
    
    def delete(self) -> "Cart":
        db.session.delete(self)
        db.session.commit()
        return self
    
    @classmethod
    def getById(cls, id: int) -> Union["Cart", None]:
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def getByPublicId(cls, publicId: str) -> Union["Cart", None]:
        return cls.query.filter_by(publicId=publicId).first()
    
    @classmethod
    def getByUser(cls, userId: int) -> Union["Cart", None]:
        return cls.query.filter_by(userId=userId).first()
    
    @classmethod
    def getAll(cls) -> List["Cart"]:
        return cls.query.all()
    
    @classmethod
    def getOrCreate(cls, userId: int) -> Tuple["Cart", bool]:
        if cart := cls.getByUser(userId):
            return cart, False
        return cls.create(userId), True
    
    def toDict(self) -> dict:
        return {
            "publicId": self.publicId,
            "userPublicId": self.user.publicId,
            "orders": [order.toDict() for order in self.orders]
        }
    
    def __repr__(self) -> str:
        return "<Cart '{}'>".format(self.user.email)


