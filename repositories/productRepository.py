from models.product import Product
from repositories.baseRepository import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, model: Product) -> None:
        super().__init__(model)


productRepository = ProductRepository(Product)
