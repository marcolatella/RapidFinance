import requests
import pandas as pd
import matplotlib.pyplot as plt
from rapidfinance import config, endpoints

from ..utils import to_dict
from .summary_info import Summary
from datetime import datetime


class Ticker:
    def __init__(self, symbol, region="US"):
        self.symbol = symbol
        self.region = region
        self.info = self.get_summary()
        self.profile_info = Summary(self.info.summaryProfile)
        self.sector = self.info.summaryProfile['sector']
        self.shortName = self.info.price['shortName']
        self.currency = self.info.price['currency']
        self.currencySymbol = self.info.price['currencySymbol']
        self.history = None

    def plot(self, columns, width=10, height=7):
        """
        It takes a list of columns, and plots them

        :param columns: a list of columns to plot
        :param width: The width of the plot in inches, defaults to 10 (optional)
        :param height: The height of the figure in inches, defaults to 7 (optional)
        """
        fig, ax = plt.subplots(figsize=(width, height))
        for col in columns:
            if col in self.history.columns:
                ax.plot(self.history[col], label=col)
        ax.legend()
        plt.show()

    def get_summary(self):
        get_req = config.yahoo_host + endpoints.summary_endpt + self.symbol
        modules = ','.join(endpoints.summary_modules)
        params = {'modules': modules}
        response = self.send_request(get_req, params)
        summary = to_dict(response.text)
        return Summary(summary['quoteSummary']['result'][0])

    def download_history(self, start, end, interval, pre_post=False, div_split=False):
        # Possible inputs for &interval=: 1m, 5m, 15m, 30m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        start = int(datetime.strptime(start, '%Y/%m/%d').timestamp())
        end = int(datetime.strptime(end, '%Y/%m/%d').timestamp())
        get_req = config.yahoo_host + endpoints.chart + self.symbol
        params = {'symbol': self.symbol, 'period1': start, 'period2': end, 'interval': interval}
        if pre_post:
            params['includePrePost'] = 'true'
        if div_split:
            params['events'] = 'div|split'
        response = self.send_request(get_req, params)

        data = to_dict(response.text)
        if data['chart']['result'] is None:
            raise Exception(data['chart']['error']['description'])

        timestamp = data['chart']['result'][0]['timestamp']
        history = {}
        for key, val in data['chart']['result'][0]['indicators']['quote'][0].items():
            history[key] = val
        if 'adjclose' in data['chart']['result'][0]['indicators']:
            history['adjclose'] = data['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
        df = pd.DataFrame(history, [datetime.fromtimestamp(x) for x in timestamp])

        self.history = df

    def __repr__(self):
        return f"Name: {self.shortName}\n" \
               f"Sector: {self.sector}\n" \
               f"Symbol: {self.symbol}\n" \
               f"Currency: {self.currency}"

    def send_request(self, req, params):
        url = req
        return requests.request("GET", url, headers=config.header, params=params)

    @property
    def summary(self):
        return f"{self.info}"

# "set-cookie:B=xxxxxxxx&b=3&s=qf; expires=Fri, 18-May-2018 00:00:00 GMT; path=/; domain=.yahoo.com"
