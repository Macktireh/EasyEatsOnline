from typing import List, Optional, Union
from uuid import uuid4
from datetime import datetime
from slugify import slugify

from app import db


class Product(db.Model):
    
    __tablename__ = "product"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicId = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128), nullable=True)
    categoryId = db.Column(db.Integer, db.ForeignKey("category.id"))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(128), nullable=True)
    description = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)
    createdAt = db.Column(db.DateTime, nullable=False)
    updatedAt = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, *args, **kwargs) -> None:
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)
    
    def save(self) -> "Product":
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def create(cls, name: str, price: float, categoryId: Optional[int] = None, image: Optional[str] = None, description: Optional[str] = None, available: Optional[bool] = True) -> "Product":
        product = cls(
            publicId=str(uuid4()),
            name=name,
            categoryId=categoryId,
            price=price,
            image=image,
            description=description,
            available=available,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        return product.save()
    
    def delete(self) -> "Product":
        db.session.delete(self)
        db.session.commit()
        return self
    
    @classmethod
    def getById(cls, id: int) -> Union["Product", None]:
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def getByPublicId(cls, publicId: str) -> Union["Product", None]:
        return cls.query.filter_by(publicId=publicId).first()
    
    @classmethod
    def getAll(cls) -> List["Product"]:
        return cls.query.all()
    
    @classmethod
    def getAllByName(cls, name: str) -> List["Product"]:
        return cls.query.filter_by(name=name).all()
    
    def toDict(self) -> dict:
        return {
            "publicId": self.publicId,
            "name": self.name,
            "price": self.price,
            "category": self.category.name if self.category else None,
            "image": self.image,
            "description": self.description,
            "available": self.available,
            "createdAt": self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": self.updatedAt.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def __repr__(self) -> str:
        return "<Product '{}'>".format(self.name)