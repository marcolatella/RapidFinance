from rapidfinance.stock import Ticker

if __name__ == '__main__':

    # period: 1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max
    # interval: 1m|2m|5m|15m|30m|60m|1d|1wk|1mo

    apple = Ticker("AAPL")
    print(apple.profile_info)

    apple.download_history(start="2005/01/01", end='2022/11/04', interval='1d')
    apple.plot(["close"])
    df = apple.history

    print(df)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
