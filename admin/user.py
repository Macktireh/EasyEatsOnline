from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class UserAdminModelView(ModelView):
    
    column_exclude_list = ['passwordHash', ]
    column_searchable_list = ['firstName', 'lastName', 'email']
    column_filters = ['isActive', 'isStaff', 'isAdmin']
    create_modal = True
    edit_modal = True
    can_export = True
    can_view_details = True
    page_size=15
    # can_create = True
    # can_edit = False
    # can_delete = False
    
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login.login'))


class UserImageAdminModelView(ModelView):
    
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login.login'))
