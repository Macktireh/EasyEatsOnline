from enum import Enum

from slugify import slugify

from app import db
from models import BaseModel


class TypeEnum(Enum):
    APPETIZER = "appetizer"
    DISH = "dish"
    DESSERT = "dessert"
    DRINK = "drink"


class Product(BaseModel):
    __tablename__ = "product"

    name = db.Column(db.String(128), nullable=False, unique=True)
    slug = db.Column(db.String(128), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(128), nullable=True)
    description = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)
    type = db.Column(db.Enum(TypeEnum), nullable=False)
    categoryId = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)

    def __init__(self, *args, **kwargs) -> None:
        if "slug" not in kwargs:
            kwargs["slug"] = slugify(kwargs.get("name", ""))
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<Product '{self.name}'>"
