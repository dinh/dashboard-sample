from flask import Flask, render_template

from .config import Config


def get_404(e):
    return render_template("home/page-404.html"), 404


application = Flask(__name__)

application.register_error_handler(404, get_404)

application.config.from_object(Config)

from apps import routes
