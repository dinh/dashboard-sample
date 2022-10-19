# Hands Off JS with HTMX

### Intro and Inspiration

There is an amazing amount of interactivity that can be achieved on a website without
needing to use `javascript`. To demonstrate this idea, this repository runs the
following site: [example site](http://dashboard.zmaytechstack.com/) with almost no `js`.
The inspiration was to implement just a few of the features that are a part
of [koyfin's](https://app.koyfin.com/) website without any `js`. And in doing so
show that you can get a lot of the same feel and functionality as a `REACT` site
or similar. I'll walk through a couple of the features but feel free to explore
the code to get a better sense of what is going on. In the appendix, setup instructions
are provided.

**Full Disclosure:** *I am using the [Alpha Vantage](https://www.alphavantage.co/) free API
and only have 5 API hits per minute, so the site does not scale well! I do my best to cache
results in S3, but only so much can be done.*

The site has the following functionality:

1. Updating the chart based on timeframe selection.
2. Search bar to search for US listed securities.
3. Polling to update the news feed every 5 minutes.

All can be seen on the homepage:

![Homepage](.images/homepage.jpg)

None of these features use `javascript` (although the table does rely on the `javascript` package Tabulator).
To allow for the response nature of the site, we use on an interesting package called
[htmx](https://htmx.org/) that is gaining in popularity rather quickly. Instead of sending json
between the server and the browser, you send html.

### An Example

They way the site uses this package can be shown with the cumulative return chart.
The following [code](https://github.com/azakmay/dashboard-sample/blob/master/apps/templates/home/macros.html)
generates the buttons along the top of the chart.

```html
{% set button_labels = ['1D', '5D', '1M', '3M', '6M', 'YTD', '1Y', '3Y', '5Y', '10Y'] %}

{% macro build_header(endpoint, target) %}
{% for button in button_labels %}
<div class="trigger-button"
     hx-post="{{ endpoint }}"
     hx-trigger="click"
     hx-indicator="#indicator"
     hx-target="{{ target }}"
     hx-vals='{"window": "{{ button }}"}'
     id="{{ button }}">{{ button }}
</div>
{% endfor %}
{% endmacro %}
```

Then in the
main [html](https://github.com/azakmay/dashboard-sample/blob/master/apps/templates/home/todays-market-grid.html)
for the homepage, the endpoint that is specified is `/chart/cum_returns`. This sends a `POST` request to the server:

```python
@application.route('/chart/cum_returns', methods=['GET', 'POST'])
def chart_cumreturns():
    view = MarketView()
    return view.get_daily_market_chart_html()
```

which uses [Plotly](https://plotly.com/python/) to build charts in `Python`
and generate html to replace the plot on the screen with an updated version.
Just like that, with no `js`, we can generate a chart with similar functionality
to that on [https://app.koyfin.com/](koyfin).

![Koyfin](.images/koyfin.jpg)

### Benefits

There are a few benefits to generate the html on the server side:

1. Language consistency: Stay in the same language as the backend code (e.g., `Python` for this example)
2. Rapid prototyping: Easier to get a bunch of visuals - think dashboards - up in less time
3. **Most Important:** No JS or front-end framework!
4. Much easier for all programmers to be full stack

### Conclusion

This is definitely not a bad approach if you're building a site and maintaining it yourself.
In fact, this isn't a bad approach for software at scale. Here is a post that recently showed up at the top
of [hackernews](https://htmx.org/essays/a-real-world-react-to-htmx-port/) about HTMX being
used for a large scale software product.

### Setup
If you would like to run this locally, you will need to setup the following environemt 
variables:
```dotenv
ASSETS_ROOT=/static/assets
STOCK_API_KEY=
DATA_BUCKET=
```

1. The API can be retrieved [here](https://www.alphavantage.co/support/#api-key)
2. The data bucket must be setup on S3 with AWS. This is used as a cheap cache to
store parquet files of data previously requested since we didn't feel like storing data
in a DB.