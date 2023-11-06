from random import choice
from typing import List

from faker import Faker

from models.product import TypeEnum
from repository.cartRepository import cartRepository
from repository.categoryRepository import categoryRepository
from repository.orderRepository import orderRepository
from repository.productRepository import productRepository
from repository.userRepository import userRepository

fake = Faker()


class Fixture:
    @classmethod
    def createUsers(cls, n: int = 5) -> List:
        return [
            userRepository.create(
                firstName=fake.first_name(),
                lastName=fake.last_name(),
                email=fake.unique.email(),
                password="password",
                isActive=i % 2 > 0,
                isStaff=i % 2 > 0,
                isAdmin=i % 2 > 0,
            )
            for i in range(n)
        ]

    @classmethod
    def createCategories(cls, n: int = 5) -> List:
        return [categoryRepository.create(name=fake.unique.word()) for _ in range(n)]

    @classmethod
    def createProducts(cls, n: int = 10, nCategories: int = 5) -> List:
        categories = cls.createCategories(nCategories)
        products = []
        for _ in range(n):
            products.append(
                productRepository.create(
                    name=fake.unique.word(),
                    price=fake.random_int(5, 1000) / 2,
                    image=fake.image_url(),
                    description=fake.text(),
                    type=choice([item.value.upper() for item in TypeEnum]),
                    categoryId=choice(categories).id if len(categories) > 0 else None,
                )
            )
        return products

    @classmethod
    def createOrders(cls, n: int = 20, nUsers: int = 5, nCategories: int = 5, nProducts: int = 10) -> List:
        users = cls.createUsers(nUsers)
        products = cls.createProducts(nProducts, nCategories)
        orders = []
        for user in users:
            order, created = orderRepository.getOrCreate(userId=user.id, productId=choice(products).id)
            if created:
                orders.append(order)
        return orders

    @classmethod
    def createCarts(cls, nUsers: int = 5, nCategories: int = 5, nProducts: int = 10, nOrders: int = 20) -> List:
        users = cls.createUsers(nUsers)
        cls.createOrders(nOrders, nUsers, nCategories, nProducts)
        carts = []
        for user in users:
            cart, _ = cartRepository.getOrCreate(userId=user.id)
            for order in orderRepository.filterAll(userId=user.id):
                if order not in cart.orders:
                    cart.orders.append(order)
                cart = cartRepository.save(cart)
            carts.append(cart)
        return carts
