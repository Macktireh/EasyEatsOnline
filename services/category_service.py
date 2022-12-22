from datetime import datetime
from typing import List, Literal, Dict, Union
from uuid import uuid4

from models.category import Category
from utils import status


class CategoryServices:
    def __init__(self) -> None:
        return
    
    @staticmethod
    def create(name) -> Category:
        return Category.create(name)
    
    @staticmethod
    def get_by_id(id: int) -> Category:
        return Category.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_publicId(publicId: str) -> Category:
        return Category.query.filter_by(publicId=publicId).first()
    
    @staticmethod
    def get_all_category() -> List[Category]:
        return Category.query.all()
    
    def update_user_by_publicId(self, data: dict, publicId: str = None) -> Union[tuple[Dict[str, str], Literal[400]], Category]:
        if not publicId or data is None:
            return {
                "status": "Fail",
                "message": "Missing paramters"
            }, status.HTTP_400_BAD_REQUEST
        category = self.get_by_publicId(publicId=publicId)
        name = data.get("name", None)
        if name:
            category.name = name
        return category.save()
