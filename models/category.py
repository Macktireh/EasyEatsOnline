from app import db
from models import BaseModel


class Category(BaseModel):
    __tablename__ = "category"

    name = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self) -> str:
        return "<Category '{}'>".format(self.name)
