from datetime import datetime
from slugify import slugify

from app import db
from models.product import Product


class Category(db.Model):
    
    __tablename__ = "category"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicId = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    product = db.relationship(Product, backref="category", cascade="all, delete, delete-orphan", single_parent=True)
    createdAt = db.Column(db.DateTime, nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __repr__(self) -> str:
        return "<Category '{}'>".format(self.name)