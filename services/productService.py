from typing import List

from flask_restx import abort
from slugify import slugify
from werkzeug import exceptions

from models.product import Product
from repositories.categoryRepository import categoryRepository
from repositories.productRepository import productRepository
from utils import status
from utils.types import RequestProductCreateOrUpdateDTO
from validators.productValidator import ProductValidator


class ProductService:
    @staticmethod
    def getAllProducts() -> List[Product]:
        return productRepository.getAll()

    @staticmethod
    def addProduct(data: RequestProductCreateOrUpdateDTO) -> Product:
        validate = ProductValidator.validate(**data)
        if validate is not True:
            abort(
                status.HTTP_400_BAD_REQUEST,
                message="The information provided is not valid",
                errors=validate,
            )

        if productRepository.filter(slug=slugify(data["name"])):
            raise exceptions.Conflict("Product already exists")

        if data.get("categoryPublicId"):
            if category := categoryRepository.getByPublicId(data.get("categoryPublicId")):
                data["categoryId"] = category.id
            data.pop("categoryPublicId")

        return productRepository.create(**data)

    @staticmethod
    def getProduct(publicId: str) -> Product:
        return productRepository.getOr404(publicId=publicId)

    @staticmethod
    def updateProduct(publicId: str, data: RequestProductCreateOrUpdateDTO) -> Product:
        product = productRepository.getOr404(publicId=publicId)

        if category := categoryRepository.getByPublicId(data.get("categoryPublicId")):
            data["categoryId"] = category.id
            data.pop("categoryPublicId")

        for key, value in data.items():
            setattr(product, key, value)

        return productRepository.save(product)

    @staticmethod
    def deleteProduct(publicId: str) -> None:
        product = productRepository.getOr404(publicId=publicId)
        productRepository.delete(product)
