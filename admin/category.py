from typing import List

from flask import redirect, url_for, Response
from flask_admin.contrib.sqla import ModelView
from flask_admin.helpers import get_form_data
from flask_login import current_user

from models.category import Category
from services.category_service import CategoryServices


class CategoryAdmin(ModelView):
    
    column_editable_list: List[str] = ['name']
    column_searchable_list: List[str] = ['name']
    column_sortable_list: List[str] = ['createdAt']
    
    form_excluded_columns: List[str] = ['publicId', 'createdAt']
    
    create_modal: bool = True
    edit_modal: bool = True
    can_export: bool = True
    can_view_details: bool = True
    page_size: int = 15
    
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs) -> Response:
        return redirect(url_for('admin_login.login'))
    
    def create_model(self, form) -> Category:
        try:
            form_data = get_form_data()
            return CategoryServices.create(form_data.get('name'))
        except:
            raise NotImplementedError()