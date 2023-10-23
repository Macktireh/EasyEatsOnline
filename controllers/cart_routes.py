from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from schemas.dto import CartDto
from services.cart_service import CartServices
from utils import status


api = CartDto.api


@api.route("")
class RetrieveCart(Resource):
    @api.response(status.HTTP_200_OK, "cart successfully retrieve.")
    @api.doc("retrieve_cart")
    @jwt_required()
    def get(self):
        """retrieve cart"""
        identity = get_jwt_identity()
        return CartServices.retrieveCart(userPublicId=identity["publicId"])

    @api.response(status.HTTP_200_OK, "cart successfully retrieve.")
    @api.doc("delete_all_orders_to_cart")
    @jwt_required()
    def delete(self):
        """delete all orders to cart"""
        identity = get_jwt_identity()
        return CartServices.deleteAllOrdersToCart(userPublicId=identity["publicId"])


@api.route("/<string:productPublicId>/add-to-cart")
class AddToCart(Resource):
    @api.response(
        status.HTTP_200_OK, "product has been successfully added to the cart."
    )
    @api.doc("add_product_to_cart")
    @jwt_required()
    def post(self, productPublicId: str):
        """add product to cart"""
        identity = get_jwt_identity()
        return CartServices.addProductToCart(
            userPublicId=identity["publicId"], productPublicId=productPublicId
        )


@api.route("/<string:productPublicId>/delete-to-cart")
class DeleteFromCart(Resource):
    @api.response(status.HTTP_200_OK, "cart successfully retrieve.")
    @api.doc("add_product_to_cart")
    @jwt_required()
    def delete(self, productPublicId: str):
        """delete product to cart"""
        identity = get_jwt_identity()
        return CartServices.deleteOrderToCart(
            userPublicId=identity["publicId"], productPublicId=productPublicId
        )
