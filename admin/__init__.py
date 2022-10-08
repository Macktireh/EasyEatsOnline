import click

from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask.cli import with_appcontext

# from services.user_service import UserServices

class HomeAdminModelView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login.login'))


class AdminModelView(ModelView):
    column_exclude_list = ['passwordHash', ]
    column_searchable_list = ['firstName', 'lastName', 'email']
    column_filters = ['isActive', 'isStaff', 'isAdmin']
    create_modal = True
    edit_modal = True
    can_export = True
    page_size=15
    # can_create = True
    # can_edit = False
    # can_delete = False
    
    def is_accessible(self):
        print(current_user.isAdmin)
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login.login'))
