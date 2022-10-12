import flask
import pandas as pd
import requests

from apps.alpha_vantage.urls import StockURLs


class SearchBuilder:
    def __init__(self):
        self.request = flask.request
        self.urls = StockURLs()

    @property
    def search_string(self):
        return self.request.args.get('q')

    def get_results(self):
        url = self.urls.get_search_url(self.search_string)
        r = requests.get(url)
        data = r.json()
        search_results = data.get('bestMatches')
        search_results = pd.DataFrame(search_results)
        if not search_results.empty:
            search_results = search_results.loc[search_results['4. region'] == 'United States', :]
        search_results = search_results.drop_duplicates('1. symbol').to_dict(orient='records')
        return search_results
