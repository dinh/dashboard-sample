from flask import render_template, redirect, url_for

from apps import application
from .views.market import MarketView
from .views.search import SearchBuilder
from .views.stock import StockView


@application.route('/')
def index():
    return redirect(url_for('todays_markets'))


@application.route('/todays_markets', methods=['GET', 'POST'])
def todays_markets():
    view = MarketView()
    fig_cumreturn = view.get_daily_market_chart_html()
    fig_drawdown = view.get_drawdown_chart_html()
    return render_template("home/todays-market-grid.html",
                           fig_drawdown=fig_drawdown,
                           fig_cumreturn=fig_cumreturn,
                           segment=view.segment)


@application.route('/chart/drawdown', methods=['GET', 'POST'])
def chart_drawdown():
    view = MarketView()
    return view.get_drawdown_chart_html()


@application.route('/chart/cum_returns', methods=['GET', 'POST'])
def chart_cumreturns():
    view = MarketView()
    return view.get_daily_market_chart_html()


@application.route('/search', methods=['GET', 'POST'])
def search():
    sb = SearchBuilder()
    return render_template('partials/search.html', search_results=sb.get_results())


@application.route('/chart/daily', methods=['GET', 'POST'])
def daily_chart():
    view = StockView()
    return view.get_daily_stock_chart_html()


@application.route('/daily')
def daily():
    view = StockView()
    return render_template("home/daily.html", fig=view.get_daily_stock_chart_html(), symbol=view.symbol,
                           segment=view.segment)
