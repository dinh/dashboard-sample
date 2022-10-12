import flask
from flask import render_template, redirect, url_for
from jinja2 import TemplateNotFound

from apps import app
from .views.market import MarketView
from .views.search import SearchBuilder
from .views.stock import StockView


@app.route('/')
def index():
    try:
        return redirect(url_for('todays_markets'))

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404


@app.route('/todays_markets', methods=['GET', 'POST'])
def todays_markets():
    view = MarketView()
    if view.is_htmx_request:
        html = view.get_daily_market_chart_html()
        resp = flask.make_response(html)
        return resp
    return render_template("home/todays-market-grid.html",
                           segment=view.segment)


@app.route('/search', methods=['GET', 'POST'])
def search():
    sb = SearchBuilder()
    return render_template('partials/search.html', search_results=sb.get_results())


@app.route('/daily/chart', methods=['GET', 'POST'])
def daily_chart():
    view = StockView()
    return view.get_daily_stock_chart_html()


@app.route('/daily')
def daily():
    view = StockView()
    return render_template("home/daily.html", fig=view.get_daily_stock_chart_html(), symbol=view.symbol,
                           segment=view.segment)
