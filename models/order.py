from datetime import datetime
from typing import List, Tuple, Union
from uuid import uuid4

from app import db


class Order(db.Model):
    
    __tablename__ = "order"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicId = db.Column(db.Text, unique=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    productId = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    ordered = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False)
    orderDate = db.Column(db.DateTime, nullable=True)
    
    def save(self) -> "Order":
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def create(cls, userId: int, productId: int, quantity: int = 1, ordered: bool = False) -> "Order":
        category = cls(
            publicId=str(uuid4()), 
            userId=userId,
            productId=productId,
            quantity=quantity,
            ordered=ordered,
            createdAt=datetime.now(), 
        )
        return category.save()
    
    def delete(self) -> "Order":
        db.session.delete(self)
        db.session.commit()
        return self
    
    @classmethod
    def getById(cls, id: int) -> Union["Order", None]:
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def getByPublicId(cls, publicId: str) -> Union["Order", None]:
        return cls.query.filter_by(publicId=publicId).first()
    
    @classmethod
    def getByUserAndProduct(cls, userId: int, productId: int, ordered: bool = False) -> Union["Order", None]:
        return cls.query.filter_by(userId=userId, productId=productId, ordered=ordered).first()
    
    @classmethod
    def getAll(cls) -> List["Order"]:
        return cls.query.all()
    
    @classmethod
    def getAllByOrdered(cls, ordered: bool) -> List["Order"]:
        return cls.query.filter_by(ordered=ordered).all()
    
    @classmethod
    def getOrCreate(cls, userId: int, productId: int) -> Tuple["Order", bool]:
        if cart := cls.getByUserAndProduct(userId=userId, productId=productId):
            return cart, False
        return cls.create(userId=userId, productId=productId), True
    
    def toDict(self) -> dict:
        return {
            "publicId": self.publicId,
            "userPublicId": self.user.publicId,
            "productPublicId": self.product.publicId,
            "quantity": self.quantity,
            "ordered": self.ordered,
            "createAt": self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "orderDate": self.orderDate.strftime("%Y-%m-%d %H:%M:%S") if self.orderDate else None,
        }
    
    def __repr__(self) -> str:
        return "<Order '{} ({})'>".format(self.product.name, self.quantity)