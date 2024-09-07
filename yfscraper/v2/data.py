from yfscraper.v2 import scraper
from yfscraper.v1 import metadata
import pandas


def _yahoo_ticker_format(ticker):
    return ticker.upper().replace(".", "-")


def _yahoo_format(tickers):
    new_tickers = []
    for ticker in tickers:
        new_tickers.append(_yahoo_ticker_format(ticker))
    return new_tickers


def download_data(tickers, base, end_date):
    tickers = _yahoo_format(tickers)
    failed = []
    data = metadata.get_metadata(base)
    for ticker in tickers:
        start_date = scraper.YAHOO_START_DATE
        if ticker in data:
            start_date = data[ticker]
        if end_date > start_date:
            df = scraper.get_price_df(ticker, start_date, end_date)
            if df.empty:
                failed.append(ticker)
            else:
                data[ticker] = end_date
                df.to_csv(base + ticker + ".csv")
    metadata.write_metadata(data, base)
    return failed


def get_data(ticker, base):
    path = base + _yahoo_ticker_format(ticker) + ".csv"
    return pandas.read_csv(path)
