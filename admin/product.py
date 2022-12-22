from typing import Any, List, Union
from slugify import slugify

from flask import redirect, url_for, Response
from flask_admin.contrib.sqla import ModelView
from flask_admin.helpers import get_form_data
from flask_login import current_user

from models.product import Product
from services.product_service import ProductServices


class ProductAdmin(ModelView):
    
    column_list: List[str] = ['publicId', 'name', 'slug', 'price', 'category.name', 'urlImage', 'description', 'available', 'createdAt', 'updatedAt']
    column_searchable_list: List[str] = ['name', 'description']
    column_filters: List[str] = ['available']
    column_sortable_list: List[str] = ['createdAt', 'updatedAt']
    column_editable_list: List[str] = ['name', 'price', 'urlImage', 'description', 'available']
    
    form_excluded_columns = ['publicId', 'slug', 'createdAt', 'updatedAt']
    
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
    
    def create_model(self, form) -> Product:
        try:
            form_data: Union[List[str], Any, None] = get_form_data()
            try:
                categoryId = int(form_data.get('category'))
            except ValueError:
                categoryId = None
            data = {
                "name": form_data.get('name'),
                "price": float(form_data.get('price')),
                "categoryId": categoryId,
                "urlImage": form_data.get('urlImage'),
                "description": form_data.get('description'),
                "available": True if form_data.get('available') else False,
            }
            return ProductServices.create(data)
        except:
            raise NotImplementedError()