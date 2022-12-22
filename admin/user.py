from typing import Dict, List

from wtforms import PasswordField, validators

from flask import redirect, url_for, Response
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin.helpers import get_form_data

from models.user import User
from services.user_service import UserServices
from utils.validators import MESSAGE_PASSWORD_INVALID, REGEX_PASSWORD_VALIDATION


class UserAdmin(ModelView):
    
    column_searchable_list : List[str] = ['firstName', 'lastName', 'email']
    column_filters : List[str] = ['isActive', 'isStaff', 'isAdmin']
    column_editable_list : List[str] = ['firstName', 'lastName', 'isActive', 'isStaff', 'isAdmin']
    column_sortable_list : List[str] = ['createdAt', 'updatedAt']
    column_exclude_list : List[str] = ['passwordHash']
    column_details_exclude_list : List[str] = ['passwordHash']
    column_export_exclude_list : List[str] = ['passwordHash']
    
    form_create_rules : List[str] = ['firstName', 'lastName', 'email', 'password', 'passwordConfirm']
    form_edit_rules : List[str] = ['firstName', 'lastName', 'isActive', 'isStaff', 'isAdmin']
    
    create_modal: bool = True
    edit_modal: bool = True
    can_export: bool = True
    can_view_details: bool = True
    page_size: int = 50
    
    form_extra_fields: Dict[str, PasswordField] = {
        'password': PasswordField('Password', [
            validators.DataRequired(),
            validators.Regexp(REGEX_PASSWORD_VALIDATION, message=MESSAGE_PASSWORD_INVALID),
        ]),
        'passwordConfirm': PasswordField('Password Confirm', [
            validators.DataRequired(),
            validators.EqualTo('password', message='Passwords must match')
        ]),
    }
    
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs) -> Response:
        return redirect(url_for('admin_login.login'))
    
    def create_model(self, form) -> User:
        try:            
            form_data = get_form_data()
            data = {
                "email": form_data.get('email'),
                "firstName": form_data.get('firstName'),
                "lastName": form_data.get('lastName'),
                "password": form_data.get('password'),
            }  
            return UserServices.create(data)
        except:
            raise NotImplementedError()