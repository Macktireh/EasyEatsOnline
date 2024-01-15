from typing import List

from flask_restx import abort
from werkzeug import exceptions

from models.order import Order
from repositories.orderRepository import orderRepository
from utils import status
from utils.types import RequestCreateOrUpdateOrderDTO
from validators.orderValidator import OrderValidator


class OrderService:
    @staticmethod
    def getAllOrders() -> List[Order]:
        return orderRepository.getAll()

    @staticmethod
    def updateQuantity(data: RequestCreateOrUpdateOrderDTO) -> Order:
        validate = OrderValidator.validate(**data)
        if validate is not True:
            abort(
                status.HTTP_400_BAD_REQUEST,
                message="The information provided is not valid",
                errors=validate,
            )

        if not (order := orderRepository.getByPublicId(data["publicId"])):
            raise exceptions.NotFound("Order not found")

        order.quantity = int(data["quantity"])
        return orderRepository.save(order)
