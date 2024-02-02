from werkzeug import exceptions

from models.cart import Cart
from repositories.cartRepository import cartRepository
from repositories.orderRepository import orderRepository
from services.productService import ProductService
from services.userService import UserService


class CartService:
    @staticmethod
    def addToCart(userPublicId: str, productPublicId: str) -> Cart:
        user = UserService.getUser(userPublicId)
        product = ProductService.getProduct(productPublicId)
        cart, _ = cartRepository.getOrCreate(userId=user.id)
        order, created = orderRepository.getOrCreate(userId=user.id, productId=product.id, ordered=False)

        if created or order not in cart.orders:
            cart.orders.append(order)
        else:
            order.quantity += 1

        orderRepository.save(order)
        return cart

    @staticmethod
    def retrieveCart(userPublicId: str) -> Cart:
        user = UserService.getUser(userPublicId)
        cart, _ = cartRepository.getOrCreate(userId=user.id)
        return cart

    @staticmethod
    def deleteFromCart(userPublicId: str, productPublicId: str) -> Cart:
        user = UserService.getUser(userPublicId)
        product = ProductService.getProduct(productPublicId)

        if not (cart := cartRepository.filter(userId=user.id)):
            raise exceptions.NotFound("Cart not found")

        if order := orderRepository.filter(userId=user.id, productId=product.id):
            orderRepository.delete(order)

        return cart

    @staticmethod
    def deleteAllFromCart(userPublicId: str) -> None:
        user = UserService.getUser(userPublicId)

        cart = cartRepository.getOr404(userId=user.id)

        for order in cart.orders:
            orderRepository.delete(order)

        cartRepository.save(cart)
