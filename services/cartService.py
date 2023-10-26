from werkzeug import exceptions

from models.cart import Cart
from repository.orderRepository import orderRepository
from repository.cartRepository import cartRepository
from services.productService import ProductService
from services.userService import UserService


class CartService:
    @staticmethod
    def addToCart(userPublicId: str, productPublicId: str) -> Cart:
        user = UserService.getUser(userPublicId)
        product = ProductService.getProduct(productPublicId)
        cart, _ = cartRepository.getOrCreate(userId=user.id)
        order, created = orderRepository.getOrCreate(
            userId=user.id, productId=product.id, ordered=False
        )

        if created or order not in cart.orders:
            cart.orders.append(order)
        else:
            order.quantity += 1

        orderRepository.save(order)
        return cart

    @staticmethod
    def retrieveCart(userPublicId: str) -> Cart:
        user = UserService.getUser(userPublicId)
        print("-" * 50)
        cart, _ = cartRepository.getOrCreate(userId=user.id)
        return cart

    @staticmethod
    def deleteFromCart(userPublicId: str, productPublicId: str) -> Cart:
        user = UserService.getUser(userPublicId)
        product = ProductService.getProduct(productPublicId)

        cart = cartRepository.filter(userId=user.id)
        if not cart:
            raise exceptions.NotFound("Cart not found")

        if order := orderRepository.filter(userId=user.id, productId=product.id):
            orderRepository.delete(order)

        return cart

    @staticmethod
    def deleteAllFromCart(userPublicId: str) -> None:
        user = UserService.getUser(userPublicId)

        cart = cartRepository.filter(userId=user.id)
        if not cart:
            raise exceptions.NotFound("Cart not found")

        for order in cart.orders:
            orderRepository.delete(order)

        cartRepository.save(cart)
