from flask import Flask, render_template

from .config import Config


def get_404(e):
    return render_template("errors/404.html"), 404


def get_500(e):
    return render_template("errors/500.html"), 500


application = Flask(__name__)

application.register_error_handler(404, get_404)
application.register_error_handler(500, get_500)

application.config.from_object(Config)

from apps import routes
