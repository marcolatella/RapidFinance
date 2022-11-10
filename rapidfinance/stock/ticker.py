import requests
import pandas as pd
import matplotlib.pyplot as plt
from rapidfinance import config, endpoints

from ..utils import to_dict
from .summary_info import Summary
from datetime import datetime


class Ticker:
    def __init__(self, symbol):
        assert isinstance(symbol, str)
        self.symbol = symbol
        self.info = self.get_summary()
        if hasattr(self.info, 'summaryProfile'):
            self.profile_info = self.info.summaryProfile
            if hasattr(self.profile_info, 'sector'):
                self.sector = self.info.summaryProfile.sector
        if hasattr(self.info.price, 'shortName'):
            self.shortName = self.info.price.shortName
        if hasattr(self.info.price, 'currency'):
            self.currency = self.info.price.currency
        if hasattr(self.info.price, 'currencySymbol'):
            self.currencySymbol = self.info.price.currencySymbol
        self.history = None

    def plot(self, columns, width=10, height=7):
        """
        It takes a list of columns, and plots them

        :param columns: a list of columns to plot
        :param width: The width of the plot in inches, defaults to 10 (optional)
        :param height: The height of the figure in inches, defaults to 7 (optional)
        """
        assert isinstance(columns, list)
        fig, ax = plt.subplots(figsize=(width, height))
        for col in columns:
            if col in self.history.columns:
                ax.plot(self.history[col], label=col)
        ax.legend()
        plt.show()

    def get_summary(self):
        """
        It takes the symbol of the stock, makes a request to Yahoo Finance, and returns a summary of the stock
        :return: A Summary object
        """
        get_req = config.yahoo_host + endpoints.summary_endpt + self.symbol
        modules = ','.join(endpoints.summary_modules)
        params = {'modules': modules}
        response = self.send_request(get_req, params)
        summary = to_dict(response.text)
        if summary['quoteSummary']['result'] is None:
            raise Exception(summary['quoteSummary']['error'])
        return Summary(summary['quoteSummary']['result'][0])

    def download_history(self, start, end, interval, pre_post=False, div_split=False):
        """
        The function takes in a start date, end date, interval, and two optional parameters (pre_post and div_split) and
        returns a pandas dataframe of the historical data.

        :param start: The start date of the history you want to download
        :param end: The end date of the data you want to download
        :param interval: 1m, 5m, 15m, 30m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        :param pre_post: Include pre-market and post-market data, defaults to False (optional)
        :param div_split: If True, the history will include dividend and split data, defaults to False (optional)
        """
        # Possible inputs for &interval=: 1m, 5m, 15m, 30m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        start = int(datetime.strptime(start, '%Y/%m/%d').timestamp())
        if end == "now":
            end = int(datetime.utcnow().timestamp())
        else:
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

    def compute_return(self, df, periods):
        returns = {}
        if isinstance(periods, list):
            for period in periods:
                returns[period] = self.__compute_return(df, period)
            return returns
        else:
            return self.__compute_return(df, periods)

    def __compute_return(self, df, period):
        assert isinstance(period, str)
        tmp = df.resample(period).agg({"open": "first",
                                       "high": "max",
                                       "low": "min",
                                       "close": "last"})
        tmp['pct_change'] = tmp.close.pct_change()
        tmp.dropna(inplace=True)
        return round(tmp.iloc[-1][-1] * 100, 2)

    def __repr__(self):
        return f"Name: {self.shortName}\n" \
               f"Symbol: {self.symbol}\n" \
               f"Currency: {self.currency}"

    def send_request(self, req, params):
        url = req
        return requests.request("GET", url, headers=config.header, params=params)

    @property
    def summary(self):
        return f"{self.info}"

# "set-cookie:B=xxxxxxxx&b=3&s=qf; expires=Fri, 18-May-2018 00:00:00 GMT; path=/; domain=.yahoo.com"
