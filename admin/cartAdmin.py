from typing import Any, List, Union
from slugify import slugify

from flask import redirect, url_for, Response
from flask_admin.contrib.sqla import ModelView
from flask_admin.helpers import get_form_data
from flask_login import current_user

from models.cart import Cart


class CartAdmin(ModelView):
    
    column_list: List[str] = ['publicId', 'user.firstName', 'user.lastName', 'orders']
    column_editable_list: List[str] = ['userId', 'orders']
    
    form_excluded_columns = ['publicId']
    
    create_modal: bool = True
    edit_modal: bool = True
    can_export: bool = True
    can_view_details: bool = True
    page_size: int = 15
    
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs) -> Response:
        return redirect(url_for('admin_login.login'))
    
    def on_model_delete(self, model):
        for order in model.orders: order.delete()
    
    def create_model(self, form) -> Cart:
        try:
            form_data = get_form_data()
            try:
                userId = int(form_data.get('user'))
            except ValueError:
                userId = None
            return Cart.create(userId)
        except:
            raise NotImplementedError()