from models.order import Order
from repositories.baseRepository import BaseRepository


class OrderRepository(BaseRepository):
    def __init__(self, model: Order) -> None:
        super().__init__(model)


orderRepository = OrderRepository(Order)
