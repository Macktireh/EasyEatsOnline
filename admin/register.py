import warnings

from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy

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


def registerAdmin(admin: Admin, db: SQLAlchemy) -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "Fields missing from ruleset", UserWarning)
        admin.add_view(UserAdmin(User, db.session))
    admin.add_view(ProductAdmin(Product, db.session))
    admin.add_view(CategoryAdmin(Category, db.session))
    admin.add_view(CartAdmin(Cart, db.session))
    admin.add_view(OrderAdmin(Order, db.session))

    # add menu items in the admin panel
    admin.add_link(MenuLink(name="API Docs", category="", url="/api"))
    admin.add_link(MenuLink(name="Logout", category="", url="/admin/auth/logout"))
