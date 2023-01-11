from typing import List, Literal, Tuple

from models.order import Order
from utils import status


class OrderServices:
    
    @staticmethod
    def getAllOrders() -> Tuple[List[Order], Literal[200]]:
        return {
            "data": [order.toDict() for order in Order.getAll()]
            }, status.HTTP_200_OK
    
    @staticmethod
    def updateQuantity(publicId: str, isAdded: bool):
        order = Order.getByPublicId(publicId)
        if order is None:
            return {
                "status": "Fail",
                "message": "Order not found"
            }, status.HTTP_404_NOT_FOUND
        if isAdded:
            order.quantity += 1
            return order.save().toDict(), status.HTTP_200_OK
        elif isAdded is False and order.quantity >= 2:
            order.quantity -= 1
            return order.save().toDict(), status.HTTP_200_OK
        return {
                "status": "Fail",
                "message":"Quantity can't be less than 1"
            }, status.HTTP_400_BAD_REQUEST 