from datetime import datetime
from typing import List, Literal, Dict, Union

from models.product import Product
from interface.product import ProductType
from utils import status


class ProductServices:
    def __init__(self) -> None:
        return
    
    @staticmethod
    def getAllProducts() -> List[Product]:
        return Product.getAll()
    
    @staticmethod
    def addProduct(data: ProductType) -> Product:
        if not data.get("price") > 0:
            return {
                "status": "Fail",
                "message": "Price must be greater than 0"
            }, status.HTTP_400_BAD_REQUEST
        return Product.create(**data)
    
    @staticmethod
    def getProductByPublicId(publicId: str) -> Product:
        if not publicId:
            return {
                "status": "Fail",
                "message": "Public ID cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        product = Product.getByPublicId(publicId)
        if not product:
            return {
                "status": "Fail",
                "message": "Product not found"
            }, status.HTTP_404_NOT_FOUND
        return product
    
    @staticmethod
    def updateProduct(publicId: str, data: ProductType) -> Product:
        if not publicId:
            return {
                "status": "Fail",
                "message": "Public ID cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        product = Product.getByPublicId(publicId)
        if not product:
            return {
                "status": "Fail",
                "message": "Product not found"
            }, status.HTTP_404_NOT_FOUND
        
        if data.get('name'):
            product.name = data.get('name')
        if data.get('description'):
            product.description = data.get('description')
        if data.get('price'):
            product.price = data.get('price')
        if data.get('categoryId'):
            product.categoryId = data.get('categoryId')
        if data.get('image'):
            product.image = data.get('image')
        if data.get('updatedAt'):
            product.updatedAt = datetime.now()
        
        return product.save()
    
    @staticmethod
    def deleteProduct(publicId: str):
        if not publicId:
            return {
                "status": "Fail",
                "message": "Public ID cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        product = Product.getByPublicId(publicId)
        if not product:
            return {
                "status": "Fail",
                "message": "Product not found"
            }, status.HTTP_404_NOT_FOUND
        
        product.delete()
        return None, status.HTTP_204_NO_CONTENT