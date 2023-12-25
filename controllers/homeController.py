from flask import Blueprint, render_template
from flask.views import View

router = Blueprint("home", __name__)


class Home(View):
    def dispatch_request(self) -> str:
        return render_template("home/home.html")


router.add_url_rule("/", view_func=Home.as_view("home"))
