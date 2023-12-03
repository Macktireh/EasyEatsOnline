from config.app import db
from models import BaseModel


class Category(BaseModel):
    __tablename__ = "category"

    name = db.Column(db.String(128), nullable=False, unique=True)
    # product = db.relationship("Product", backref="category", uselist=True, lazy="joined")

    def __repr__(self) -> str:
        return f"<Category '{self.name}'>"
