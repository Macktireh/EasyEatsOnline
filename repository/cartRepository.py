from models.cart import Cart
from repository.baseRepository import BaseRepository


class CartRepository(BaseRepository):
    def __init__(self, model: Cart) -> None:
        super().__init__(model)


cartRepository = CartRepository(Cart)
