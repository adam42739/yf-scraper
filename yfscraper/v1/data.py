from yfscraper.v1 import scraper
import os
from yfscraper.v1 import metadata
import datetime
import pandas


def download_data(tickers, downloads, base):
    data = metadata.get_metadata(base)
    failed = scraper.download_tickers(tickers, downloads)
    for ticker in tickers:
        if ticker not in failed:
            cur_path = scraper.download_ticker_path(ticker, downloads)
            new_path = scraper.download_ticker_path(ticker, base)
            os.rename(cur_path, new_path)
            data[ticker] = datetime.datetime.today()
    metadata.write_metadata(data, base)
    return failed

def get_data(ticker, base):
    path = scraper.download_ticker_path(ticker, base)
    return pandas.read_csv(path)
