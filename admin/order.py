from typing import Any, List, Union
from slugify import slugify

from flask import redirect, url_for, Response
from flask_admin.contrib.sqla import ModelView
from flask_admin.helpers import get_form_data
from flask_login import current_user

from models.order import Order


class OrderAdmin(ModelView):
    
    column_list: List[str] = ['publicId', 'user.firstName', 'user.lastName', 'product.name', 'quantity', 'ordered', 'createdAt', 'orderDate']
    column_filters: List[str] = ['ordered', 'quantity']
    column_sortable_list: List[str] = ['createdAt', 'orderDate']
    column_editable_list: List[str] = ['quantity', 'ordered', 'orderDate']
    
    form_excluded_columns = ['publicId', 'ordered', 'createdAt']
    
    create_modal: bool = True
    edit_modal: bool = True
    can_export: bool = True
    can_view_details: bool = True
    page_size: int = 15
    
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs) -> Response:
        return redirect(url_for('admin_login.login'))
    
    def on_model_change(self, form, model, is_created) -> None:
        if is_created and not model.slug:
            model.slug = slugify(model.name)
        else:
            if model.slug != slugify(model.name):
                model.slug = slugify(model.name)
    
    def create_model(self, form) -> Order:
        try:
            form_data = get_form_data()
            try:
                userId = int(form_data.get('user'))
            except ValueError:
                userId = None
            try:
                productId = int(form_data.get('product'))
            except ValueError:
                productId = None
            data = {
                "userId": userId,
                "productId": productId,
                "quantity": int(form_data.get('quantity')) if form_data.get('quantity') else 1,
            }
            return Order.create(**data)
        except:
            raise NotImplementedError()