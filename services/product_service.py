from datetime import datetime
from typing import List, Literal, Dict, Union
from uuid import uuid4
from slugify import slugify

from models.product import Product
from utils import status


class ProductServices:
    def __init__(self) -> None:
        return
    
    @staticmethod
    def create(data) -> Product:
        
        product = Product(
                publicId=str(uuid4()),
                name=data.get('name'),
                slug=slugify(data.get('name')),
                price=float(data.get('price')),
                categoryId=data.get('categoryId'),
                urlImage=data.get('urlImage'),
                description=data.get('description'),
                available=True if data.get('available') else False,
                createdAt=datetime.now(),
                updatedAt=datetime.now(),
            )
        return product.save()
    
    @staticmethod
    def get_by_id(id: int) -> Product:
        return Product.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_publicId(publicId: str) -> Product:
        return Product.query.filter_by(publicId=publicId).first()
    
    @staticmethod
    def get_all_products() -> List[Product]:
        return Product.query.all()
    
    def update_product_by_publicId(self, data: dict, publicId: str = None) -> Union[tuple[Dict[str, str], Literal[400]], Product]:
        if not publicId or data is None:
            return {
                "status": "Fail",
                "message": "Missing paramters"
            }, status.HTTP_400_BAD_REQUEST
        product = self.get_by_publicId(publicId=publicId)
        name = data.get("name", None)
        urlImage = data.get("urlImage", None)
        description = data.get("description", None)
        available = data.get("available", None)
        if name:
            product.name = name
        if urlImage:
            product.urlImage = urlImage
        if description:
            product.description = description
        if available is True or available is False:
            product.available = available
        return product.save()
