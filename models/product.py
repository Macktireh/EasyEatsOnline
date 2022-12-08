import uuid
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
    urlImage = db.Column(db.String(128), nullable=True)
    description = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)
    createdAt = db.Column(db.DateTime, nullable=False)
    updatedAt = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __repr__(self) -> str:
        return "<Product '{}'>".format(self.name)