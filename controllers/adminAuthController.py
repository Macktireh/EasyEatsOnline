from typing import Union

from flask import Blueprint, render_template, url_for, redirect, flash, request, Response
from flask_login import login_user, logout_user

from services.authService import AuthService


adminLogin = Blueprint("adminLogin", __name__)


@adminLogin.route("/admin/auth/login", methods=["GET", "POST"])
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


@adminLogin.route("/admin/auth/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("home"))
