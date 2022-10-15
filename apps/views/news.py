import flask

from apps.alpha_vantage.api import AlphaVantage


class NewsView:

    def __init__(self):
        self.request = flask.request
        self.av = AlphaVantage()

    @property
    def tickers(self):
        return self.request.args.get('tickers')

    @property
    def topics(self):
        return self.request.args.get('topics')

    def get_news_feed(self):
        newskwargs = {}
        if self.tickers:
            newskwargs['tickers'] = self.tickers
        if self.topics:
            newskwargs['topics'] = self.topics
        return self.av.get_news_feed(**newskwargs)
