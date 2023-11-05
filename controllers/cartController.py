from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from schemas.cartSchema import CartSchema
from services.cartService import CartService
from utils import status

api = CartSchema.api


@api.route("")
class RetrieveOrDeleteAllFromCart(Resource):
    @api.response(status.HTTP_200_OK, "cart successfully retrieve.")
    @api.doc("retrieve_cart")
    @api.marshal_with(CartSchema.cart)
    @jwt_required()
    def get(self):
        """retrieve cart"""
        identity = get_jwt_identity()
        return CartService.retrieveCart(identity["publicId"])

    @api.response(status.HTTP_204_NO_CONTENT, "cart successfully deleted.")
    @api.doc("delete_all_from_cart")
    @jwt_required()
    def delete(self):
        """delete all orders to cart"""
        identity = get_jwt_identity()
        return CartService.deleteAllFromCart(identity["publicId"]), status.HTTP_204_NO_CONTENT


@api.route("/add-to-cart/<string:productPublicId>")
class AddToCart(Resource):
    @api.response(status.HTTP_201_CREATED, "product has been successfully added to the cart.")
    @api.doc("add_product_to_cart")
    @api.marshal_with(CartSchema.cart)
    @jwt_required()
    def post(self, productPublicId: str):
        """add product to cart"""
        identity = get_jwt_identity()
        return CartService.addToCart(identity["publicId"], productPublicId)


@api.route("/delete-to-cart/<string:productPublicId>")
class DeleteFromCart(Resource):
    @api.response(status.HTTP_204_NO_CONTENT, "product has been successfully deleted from the cart.")
    @api.doc("add_product_to_cart")
    @api.marshal_with(CartSchema.cart)
    @jwt_required()
    def delete(self, productPublicId: str):
        """delete product to cart"""
        identity = get_jwt_identity()
        return CartService.deleteFromCart(identity["publicId"], productPublicId), status.HTTP_204_NO_CONTENT
