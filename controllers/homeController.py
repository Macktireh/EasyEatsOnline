from pprint import pprint

from flask import Blueprint, current_app, render_template
from flask.views import View

router = Blueprint("home", __name__, template_folder="../templates", static_folder="../../static")


class Home(View):
    def dispatch_request(self) -> str:
        print()
        pprint(current_app.config)
        print()
        return render_template("home/home.html")


router.add_url_rule("/", view_func=Home.as_view("home"))
