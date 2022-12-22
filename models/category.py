from datetime import datetime
from typing import List
from uuid import uuid4

from app import db
from models.product import Product


class Category(db.Model):
    
    __tablename__ = "category"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicId = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    product = db.relationship(Product, backref="category", cascade="all, delete, delete-orphan", single_parent=True)
    createdAt = db.Column(db.DateTime, nullable=False)
    
    def save(self) -> "Category":
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def create(cls, name: str) -> "Category":
        category = cls(publicId=str(uuid4()), name=name, createdAt=datetime.now())
        return category.save()
    
    def delete(self) -> "Category":
        db.session.delete(self)
        db.session.commit()
        return self
    
    @classmethod
    def getById(cls, id: int) -> "Category":
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def getByPublicId(cls, publicId: str) -> "Category":
        return cls.query.filter_by(publicId=publicId).first()
    
    @classmethod
    def getByName(cls, name: str) -> "Category":
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def getAll(cls) -> list:
        return cls.query.all()
    
    @classmethod
    def getAllByName(cls, name: str) -> List["Category"]:
        return cls.query.filter_by(name=name).all()
    
    def __repr__(self) -> str:
        return "<Category '{}'>".format(self.name)