from models.cart import Cart
from repositories.baseRepository import BaseRepository


class CartRepository(BaseRepository):
    def __init__(self, model: Cart) -> None:
        super().__init__(model)


cartRepository = CartRepository(Cart)
