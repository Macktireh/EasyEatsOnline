from typing import List

from werkzeug import exceptions

from models.category import Category
from repositories.categoryRepository import categoryRepository
from utils.types import RequestCategoryCreateOrUpdateDTO


class CategoryService:
    @staticmethod
    def getAllCategories() -> List[Category]:
        return categoryRepository.getAll()

    @staticmethod
    def addCategory(data: RequestCategoryCreateOrUpdateDTO) -> Category:
        if not data["name"]:
            raise exceptions.BadRequest("Category name cannot be empty")

        if _ := categoryRepository.filter(name=data["name"]):
            raise exceptions.Conflict("Category already exists")

        return categoryRepository.create(name=data["name"])

    @staticmethod
    def getCategory(publicId: str) -> Category:
        if not (category := categoryRepository.getByPublicId(publicId)):
            raise exceptions.NotFound("Category not found")
        return category

    @staticmethod
    def updateCategory(publicId: str, data: RequestCategoryCreateOrUpdateDTO) -> Category:
        if not (category := categoryRepository.getByPublicId(publicId)):
            raise exceptions.NotFound("Category not found")
        category.name = data.get("name", category.name)
        return categoryRepository.save(category)

    @staticmethod
    def deleteCategory(publicId: str) -> None:
        if not (category := categoryRepository.getByPublicId(publicId)):
            raise exceptions.NotFound("Category not found")
        categoryRepository.delete(category)
