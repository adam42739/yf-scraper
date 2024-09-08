from yfscraper.v2 import scraper
from yfscraper.v1 import metadata
import pandas
import os


def yahoo_ticker_format(ticker):
    return ticker.upper().replace(".", "-")


def yahoo_format(tickers):
    new_tickers = []
    for ticker in tickers:
        new_tickers.append(yahoo_ticker_format(ticker))
    return new_tickers


def _update_price_file(ticker, df, base):
    path = base + ticker + ".csv"
    if os.path.exists(path):
        df_old = get_data(ticker, base)
        df = pandas.concat([df, df_old])
        df = df.drop_duplicates(subset="Date", keep="last")
        df = df.sort_values(by=["Date"], ascending=False)
        df.to_csv(path, index=False)
    else:
        df.to_csv(path, index=False)


def download_data(tickers, base, end_date):
    tickers = yahoo_format(tickers)
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
                _update_price_file(ticker, df, base)
    metadata.write_metadata(data, base)
    return failed


def get_data(ticker, base):
    path = base + yahoo_ticker_format(ticker) + ".csv"
    df = pandas.read_csv(path)
    df["Date"] = pandas.to_datetime(df["Date"])
    return df
