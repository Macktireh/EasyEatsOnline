from datetime import datetime
from uuid import uuid4
from slugify import slugify

from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.helpers import get_form_data
from flask_login import current_user


class ProductAdminModelView(ModelView):
    
    column_searchable_list = ['name', 'description']
    column_filters = ['available']
    column_sortable_list = ['createdAt', 'updatedAt']
    column_editable_list = ['name', 'price', 'urlImage', 'description', 'available']
    
    form_excluded_columns = ['publicId', 'createdAt', 'updatedAt']
    
    create_modal = True
    edit_modal = True
    can_export = True
    can_view_details = True
    page_size=15
    
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login.login'))
    
    def on_model_change(self, form, model, is_created) -> None:
        if is_created and not model.slug:
            model.slug = slugify(model.name)
        else:
            if model.slug != slugify(model.name):
                model.slug = slugify(model.name)
    
    def create_model(self, form):
        data = get_form_data()
        try:
            from models.product import Product
            
            product = Product(
                publicId=str(uuid4()),
                name=data.get('name'),
                slug=slugify(data.get('name')) if data.get('name') else "",
                price=float(data.get('price')),
                urlImage=data.get('urlImage'),
                description=data.get('description'),
                available=True if data.get('available') else False,
                updatedAt=datetime.utcnow(),
            )
            return product.save()
        except:
            raise NotImplementedError()