# Hands Off JS with HTMX

### Intro and Inspiration

There is an amazing amount of interactivity that can be achieved on a website without
needing to use `JavaScript`. To demonstrate this idea, this repository runs the
following [site](http://dashboard.zmaytechstack.com/) with almost no `js`.
There were a few goals in mind:

1. Implement just a few of the features that are a part
   of [koyfin's](https://app.koyfin.com/) website without any `js` and in doing so
   show that you can get a lot of the same feel and functionality as a site using a
   front-end `js` library (e.g., `REACT`).
2. Show a more robust example than is typically found, but that is also very simple
   and easy to follow.
3. Minimal `JavaScript` Dependencies. Only three were needed:
   1. [HTMX](https://htmx.org/)
   2. [Plotly](https://plotly.com/python/)
   3. [Tabulator](http://tabulator.info/)

We will walk through a couple of the features but I'd encourage those interested
to explore the code to get a better sense of what is going on.
Setup instructions are provided in the appendix.

**Full Disclosure:** *I am using the [Alpha Vantage](https://www.alphavantage.co/) free API
and only have 5 API hits per minute, so you can imagine that the site does not scale well!
I do my best to cache results in S3, but only so much can be done.*

The site has the following functionality without javascript:

1. Updating the chart based on timeframe selection.
2. Search bar to search for US listed securities.
3. Polling to update the news feed every 5 minutes.

All can be seen on the homepage:

![Homepage](.images/homepage.jpg)

None of these features use `javascript` (although the table does rely on the `javascript` package Tabulator).
To generate server-side requests, we use the [htmx](https://htmx.org/) package.
Instead of sending json between the server and the browser, you send html and make
server-side requests directly in the html: `<a hx-post="/click">Click Me!</a>`.

### An Example

The way the site uses this package can be shown with the cumulative return chart on the
landing page.The
following [code](https://github.com/azakmay/dashboard-sample/blob/master/apps/templates/home/macros.html)
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
for the homepage, the endpoint that is specified is `/chart/cum_returns` and it sends a `POST` request here:

```python
@application.route('/chart/cum_returns', methods=['GET', 'POST'])
def chart_cumreturns():
    view = MarketView()
    return view.get_daily_market_chart_html()
```

This uses endpoint uses [Plotly](https://plotly.com/python/) to build charts in
`Python` and generates html to replace the plot on the screen with an updated version.
Just like that, with no `js`, we can generate a chart with similar functionality
to that on [https://app.koyfin.com/](koyfin).

![Koyfin](.images/koyfin.jpg)

### Benefits

There are a few benefits to generating the html on the server side:

1. Language consistency: Stay in the same language as the backend code (e.g., `Python` used here)
2. Rapid prototyping: Easier to get a bunch of visuals - think dashboards - up in less time
3. Easier for all programmers to be full stack
4. **Most Important:** No JS or front-end framework!

### Conclusion

Mission accomplished!

![Languages](.images/github-languages.jpg)

This is not a bad approach if you're building a site and maintaining it yourself.
In fact, this isn't a bad approach for software at scale. Here is a post that recently showed up at the top
of [hackernews](https://htmx.org/essays/a-real-world-react-to-htmx-port/) about HTMX being
used for a large scale software product.

## Appendix

### Setup

If you would like to run this locally, you will need to setup the following environment
variables:

```dotenv
STOCK_API_KEY
DATA_BUCKET
```

1. The API can be retrieved [here](https://www.alphavantage.co/support/#api-key)
2. The data bucket must be setup on S3 with AWS. This is used as a cheap cache to
   store parquet files of data previously requested since we didn't feel like storing data
   in a DB.

As long as you setup these environment variables, you should be able to setup a virtual
environment, `pip install -r requirements.txt` and be good to go.

### Tools and Tech

1. Htmx
2. Flask
3. CSS: Mostly Grid and Flex
4. Alpha Vantage API
5. AWS S3 and Elastic Beanstalk
