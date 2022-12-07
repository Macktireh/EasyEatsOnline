from datetime import datetime
from uuid import uuid4

from wtforms import PasswordField, validators

from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin.helpers import get_form_data

from utils.validators import REGEX_PASSWORD_VALIDATION


class UserAdminModelView(ModelView):
    
    column_searchable_list = ['firstName', 'lastName', 'email']
    column_filters = ['isActive', 'isStaff', 'isAdmin']
    column_editable_list = ['firstName', 'lastName', 'isActive', 'isStaff', 'isAdmin']
    column_sortable_list = ['createdAt', 'updatedAt']
    column_exclude_list = ['passwordHash']
    column_details_exclude_list = column_exclude_list
    column_export_exclude_list = column_exclude_list
    
    form_excluded_columns = ['publicId', 'passwordHash', 'createdAt', 'updatedAt']
    form_edit_rules = column_filters
    
    create_modal = True
    edit_modal = True
    can_export = True
    can_view_details = True
    
    page_size=15
    form_extra_fields = {
        'password': PasswordField('Password', [
            validators.DataRequired(),
            validators.Regexp(REGEX_PASSWORD_VALIDATION),
            validators.EqualTo('passwordConfirm', message='Passwords must match')
        ]),
        'passwordConfirm': PasswordField('Password Confirm', [
            validators.DataRequired(),
            validators.Regexp(REGEX_PASSWORD_VALIDATION),
            validators.EqualTo('password', message='Passwords must match')
        ]),
    }
    
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login.login'))
    
    def create_model(self, form):
        data = get_form_data()
        try:
            from models.user import User
            
            new_user = User(
                publicId=str(uuid4()),
                email=data.get('email'),
                firstName=data.get('firstName'),
                lastName=data.get('lastName'),
                password=data.get('password'),
                isActive=True if data.get('isActive') else False,
                isStaff=True if data.get('isStaff') else False,
                isAdmin=True if data.get('isAdmin') else False,
                updatedAt=datetime.utcnow(),
            )
            return new_user.save()
        except:
            raise NotImplementedError()