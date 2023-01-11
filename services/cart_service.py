from models.cart import Cart
from models.user import User
from models.product import Product
from models.order import Order
from utils import status


class CartServices:
    
    @staticmethod
    def addProductToCart(userPublicId: str, productPublicId: str):
        if not userPublicId:
            return {
                "status": "Fail",
                "message": "User Public ID cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        if not productPublicId:
            return {
                "status": "Fail",
                "message": "Product Public ID cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        user = User.getByPublicId(userPublicId)
        if not user:
            return {
                "status": "Fail",
                "message": "User not found"
            }, status.HTTP_404_NOT_FOUND
        
        product = Product.getByPublicId(productPublicId)
        if not product:
            return {
                "status": "Fail",
                "message": "Product not found"
            }, status.HTTP_404_NOT_FOUND
        
        cart, _ = Cart.getOrCreate(user.id)
        order, created = Order.getOrCreate(userId=user.id, productId=product.id)
        
        if created:
            cart.orders.append(order)
            order.save()
        elif order not in cart.orders:
            cart.orders.append(order)
            order.save()
        else:
            order.quantity += 1
            order.save()
        
        return cart.toDict(), status.HTTP_200_OK
    
    @staticmethod
    def retrieveCart(userPublicId: str):
        user = User.getByPublicId(userPublicId)
        if not user:
            return {
                "status": "Fail",
                "message": "User not found"
            }, status.HTTP_404_NOT_FOUND
        
        cart = Cart.getByUser(user.id)
        if not cart:
            cart = Cart.create(user.id)
        return cart.toDict(), status.HTTP_200_OK
    
    @staticmethod
    def deleteOrderToCart(userPublicId: str, productPublicId: str):
        if not userPublicId:
            return {
                "status": "Fail",
                "message": "User Public ID cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        if not productPublicId:
            return {
                "status": "Fail",
                "message": "Product Public ID cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        user = User.getByPublicId(userPublicId)
        if not user:
            return {
                "status": "Fail",
                "message": "User not found"
            }, status.HTTP_404_NOT_FOUND
        
        product = Product.getByPublicId(productPublicId)
        if not product:
            return {
                "status": "Fail",
                "message": "Product not found"
            }, status.HTTP_404_NOT_FOUND
        
        cart = Cart.getByUser(user.id)
        if not cart:
            return {
                "status": "Fail",
                "message": "Cart not found"
            }, status.HTTP_400_BAD_REQUEST
        
        if order := Order.getByUserAndProduct(userId=user.id, productId=product.id):
            order.delete()
        
        return cart.toDict(), status.HTTP_200_OK
    
    @staticmethod
    def deleteAllOrdersToCart(userPublicId: str):
        if not userPublicId:
            return {
                "status": "Fail",
                "message": "User Public ID cannot be empty"
            }, status.HTTP_400_BAD_REQUEST
        
        user = User.getByPublicId(userPublicId)
        if not user:
            return {
                "status": "Fail",
                "message": "User not found"
            }, status.HTTP_404_NOT_FOUND
        
        cart = Cart.getByUser(user.id)
        if not cart:
            return {
                "status": "Fail",
                "message": "Cart not found"
            }, status.HTTP_400_BAD_REQUEST
        
        for order in cart.orders: order.delete()
        cart.orders.clear()
        cart.save()
        
        return cart.toDict(), status.HTTP_200_OK