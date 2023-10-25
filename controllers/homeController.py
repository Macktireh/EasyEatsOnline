from flask import Blueprint, Response, render_template


homeRoute = Blueprint("home", __name__)


@homeRoute.route("/")
def home() -> Response:
    return render_template("home/home.html")
