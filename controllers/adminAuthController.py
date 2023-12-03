from typing import Union

from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from services.authService import AuthService

router = Blueprint("adminLogin", __name__)


@router.route("/admin/auth/login", methods=["GET", "POST"])
def login() -> Union[Response, str]:
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email and password:
            user = AuthService.authenticate(email, password)
            if user and user.isActive and user.isStaff and user.isAdmin:
                login_user(user)
                return redirect(url_for("admin.index"))
        flash("Please fill in the 'email' and 'password' fields for an administrator account.")
    return render_template("admin/login.html")


@router.route("/admin/auth/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("web.home.home"))
