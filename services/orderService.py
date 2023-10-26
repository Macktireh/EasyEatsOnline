from typing import List

from werkzeug import exceptions
from flask_restx import abort

from dto import RequestCreateOrUpdateOrder
from models.order import Order
from repository.orderRepository import orderRepository
from utils import status
from validators.orderValidator import OrderValidator


class OrderService:
    @staticmethod
    def getAllOrders() -> List[Order]:
        return orderRepository.getAll()

    @staticmethod
    def updateQuantity(data: RequestCreateOrUpdateOrder) -> Order:
        validate = OrderValidator.validate(**data)
        if validate is not True:
            abort(status.HTTP_400_BAD_REQUEST, message="The information provided is not valid", errors=validate)

        order = orderRepository.getByPublicId(data["publicId"])
        if not order:
            raise exceptions.NotFound("Order not found")

        order.quantity = int(data["quantity"])
        return orderRepository.save(order)
