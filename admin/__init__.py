from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_login import current_user


class HomeAdminModelView(AdminIndexView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.isActive and current_user.isStaff and current_user.isAdmin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin_login.login"))
