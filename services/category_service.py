from typing import List, Literal, Tuple

from models.category import Category
from models.types import CategoryType
from utils import status


class CategoryServices:
    
    @staticmethod
    def getAllCategories() -> Tuple[List[Category], Literal[200]]:
        return Category.getAll(), status.HTTP_200_OK
    
    @staticmethod
    def addCategory(data: CategoryType) -> Category:
        if data.get('publicId') or data.get('createdAt') or data.get('updatedAt'):
            return {
                "status": "Fail",
                "message": "PublicId, createdAt and updatedAt are read only"
            }, status.HTTP_400_BAD_REQUEST
        
        category = Category.create(**data)
        return category.toDict(), status.HTTP_201_CREATED
    
    @staticmethod
    def getCategoryByPublicId(publicId: str):
        if not publicId:
            return {
                "status": "Fail",
                "message": "Parameter publicId cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        category = Category.getByPublicId(publicId)
        if not category:
            return {
                "status": "Fail",
                "message": "Category not found"
            }, status.HTTP_404_NOT_FOUND
        return category.toDict(), status.HTTP_200_OK
    
    @staticmethod
    def updateCategoryByPublicId(publicId: str, data: CategoryType):
        if not publicId:
            return {
                "status": "Fail",
                "message": "Parameter publicId cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        category = Category.getByPublicId(publicId)
        if not category:
            return {
                "status": "Fail",
                "message": "Category not found"
            }, status.HTTP_404_NOT_FOUND
        
        if data.get('publicId') or data.get('createdAt') or data.get('updatedAt'):
            return {
                "status": "Fail",
                "message": "PublicId, createdAt and updatedAt are read only"
            }, status.HTTP_400_BAD_REQUEST
        
        if data.get("name"):
            category.name = data.get("name")
        
        category.save()
        return category.toDict(), status.HTTP_200_OK
    
    @staticmethod
    def deleteCategoryByPublicId(publicId: str):
        if not publicId:
            return {
                "status": "Fail",
                "message": "Parameter publicId cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        category = Category.getByPublicId(publicId)
        if not category:
            return {
                "status": "Fail",
                "message": "Category not found"
            }, status.HTTP_404_NOT_FOUND
        
        category.delete()
        return None, status.HTTP_204_NO_CONTENT