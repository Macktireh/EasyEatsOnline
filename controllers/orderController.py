from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from schemas.orderSchema import OrderSchema
from services.orderService import OrderService
from utils import status


api = OrderSchema.api


@api.route("")
class ListOrder(Resource):
    @api.response(status.HTTP_200_OK, "List of orders successfully.")
    @api.doc("list_of_order")
    @api.marshal_list_with(OrderSchema.order, envelope="data")
    @jwt_required()
    def get(self):
        """list of orders"""
        return OrderService.getAllOrders()


@api.route("/update-quantity")
class UpdateQuantityOrder(Resource):
    @api.response(status.HTTP_200_OK, "update quantity of order successfully.")
    @api.doc("update_quantity_of_order")
    @api.marshal_list_with(OrderSchema.order)
    @api.expect(OrderSchema.updateQuantityOrder, validate=True)
    @jwt_required()
    def patch(self):
        """update quantity of order"""
        return OrderService.updateQuantity(request.json)
