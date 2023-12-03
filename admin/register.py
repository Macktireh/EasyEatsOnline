import warnings

from flask import Flask
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy

from admin import HomeAdminModelView
from admin.cartAdmin import CartAdmin
from admin.categoryAdmin import CategoryAdmin
from admin.orderAdmin import OrderAdmin
from admin.productAdmin import ProductAdmin
from admin.userAdmin import UserAdmin
from models.cart import Cart
from models.category import Category
from models.order import Order
from models.product import Product
from models.user import User


def registerAdmin(app: Flask, db: SQLAlchemy) -> None:
    admin = Admin(app, index_view=HomeAdminModelView(name="Overview"), name="Control Panel")

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "Fields missing from ruleset", UserWarning)
        admin.add_view(UserAdmin(User, db.session))

    admin.add_view(CategoryAdmin(Category, db.session))
    admin.add_view(ProductAdmin(Product, db.session))
    admin.add_view(CartAdmin(Cart, db.session))
    admin.add_view(OrderAdmin(Order, db.session))

    admin.add_link(MenuLink(name="API Docs", category="", url="/api/docs"))
    admin.add_link(MenuLink(name="Logout", category="", url="/admin/auth/logout"))
