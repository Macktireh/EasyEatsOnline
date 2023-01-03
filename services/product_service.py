from datetime import datetime
from typing import List, Literal, Tuple
from models.category import Category

from models.product import Product
from models.types import ProductType
from utils import status


class ProductServices:
    
    @staticmethod
    def getAllProducts() -> Tuple[List[Product], Literal[200]]:
        return Product.getAll(), status.HTTP_200_OK
    
    @staticmethod
    def addProduct(data: ProductType):
        if not data.get("price") > 0:
            return {
                "status": "Fail",
                "message": "Price must be greater than 0"
            }, status.HTTP_400_BAD_REQUEST
        
        if data.get('categoryPublicId'):
            category = Category.getByPublicId(data.get('categoryPublicId'))
            if not category:
                return {
                    "status": "Fail",
                    "message": f"Category does not exist"
                    }, status.HTTP_404_NOT_FOUND
            else:
                data.pop('categoryPublicId')
                data.update({
                    "categoryId": category.id if category else None
                })
        
        if data.get('publicId') or data.get('createdAt') or data.get('updatedAt'):
            return {
                "status": "Fail",
                "message": "PublicId, createdAt and updatedAt are read only"
            }, status.HTTP_400_BAD_REQUEST
        
        product = Product.create(**data)
        return product.toDict(), status.HTTP_201_CREATED
    
    @staticmethod
    def getProductByPublicId(publicId: str):
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
        return product.toDict(), status.HTTP_200_OK
    
    @staticmethod
    def updateProductByPublicId(publicId: str, data: ProductType):
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
        
        if data.get('publicId') or data.get('createdAt') or data.get('updatedAt'):
            return {
                "status": "Fail",
                "message": "PublicId, createdAt and updatedAt are read only"
            }, status.HTTP_400_BAD_REQUEST
        
        if data.get('name'):
            product.name = data.get('name')
        if data.get('description'):
            product.description = data.get('description')
        if data.get('price'):
            product.price = data.get('price')
        if data.get('categoryPublicId'):
            category = Category.getByPublicId(data.get('categoryPublicId'))
            if not category:
                return {
                    "status": "Fail",
                    "message": f"Category does not exist"
                    }, status.HTTP_404_NOT_FOUND
            product.categoryId = category.id
        if data.get('image'):
            product.image = data.get('image')
        if data.get('updatedAt'):
            product.updatedAt = datetime.now()
        
        return product.save().toDict(), status.HTTP_200_OK
    
    @staticmethod
    def deleteProductByPublicId(publicId: str):
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