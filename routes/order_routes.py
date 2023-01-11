from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from schemas.dto import OrderDto
from services.order_service import OrderServices
from utils import status


api = OrderDto.api


@api.route('')
class ListOrder(Resource):
    
    @api.response(status.HTTP_200_OK, 'List of orders successfully.')
    @api.doc('list_of_order')
    @jwt_required()
    def get(self):
        """list of orders"""
        return OrderServices.getAllOrders()


@api.route('/<string:publicId>/update-quantity')
class UpdateQuantityOrder(Resource):
    
    @api.response(status.HTTP_200_OK, 'update quantity of order successfully.')
    @api.doc('update_quantity_of_order')
    @api.expect(OrderDto.IUpdateQuantityOrder, validate=True)
    @jwt_required()
    def post(self, publicId: str):
        """update quantity of order"""
        return OrderServices.updateQuantity(publicId=publicId, isAdded=request.json['isAdded'])