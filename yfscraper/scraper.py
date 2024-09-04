from selenium.webdriver import Chrome
import datetime
import time
import os
import tqdm

YAHOO_START_DATE = datetime.datetime(1970, 1, 1)
YAHOO_DATE_ITER = 86400


def _yahoo_date_number(date):
    return (date - YAHOO_START_DATE).days * YAHOO_DATE_ITER


YAHOO_LINK1 = "https://query1.finance.yahoo.com/v7/finance/download/"
YAHOO_LINK2 = "?period1="
YAHOO_LINK3 = "&period2="
YAHOO_LINK4 = "&interval=1d&events=history&includeAdjustedClose=true"


def _yahoo_url(ticker, start_date, end_date):
    return (
        YAHOO_LINK1
        + _yahoo_ticker_format(ticker)
        + YAHOO_LINK2
        + str(_yahoo_date_number(start_date))
        + YAHOO_LINK3
        + str(_yahoo_date_number(end_date))
        + YAHOO_LINK4
    )


def _yahoo_ticker_format(ticker):
    return ticker.upper().replace(".", "-")


class _Driver:

    def __init__(self):
        self._driver = Chrome()

    def __del__(self):
        self._driver.quit()

    def download_ticker(self, ticker, start_date, end_date, wait_time):
        url = _yahoo_url(ticker, start_date, end_date)
        self._driver.get(url)
        time.sleep(wait_time)


def _download_tickers_control(driver, stocks, wait_time):
    for ticker in tqdm.tqdm(stocks):
        driver.download_ticker(
            ticker, stocks[ticker]["start_date"], stocks[ticker]["end_date"], wait_time
        )


def _rm_crdownload(stocks, downloads):
    for ticker in stocks:
        path = downloads + _yahoo_ticker_format(ticker) + ".crdownload"
        if os.path.exists(path):
            os.remove(path)


def _exists(ticker, downloads):
    return os.path.exists(downloads + _yahoo_ticker_format(ticker) + ".csv")


def _get_failed(stocks, downloads):
    failed = []
    for ticker in stocks:
        if not _exists(ticker, downloads):
            failed.append(ticker)
    return failed


WAIT_TIME_FAST = 0.3
WAIT_TIME_SLOW1 = 1
WAIT_TIME_SLOW2 = 5


def download_tickers(stocks, downloads):
    driver = _Driver()
    print("DOWNLOAD TICKERS PART 1/3: ")
    _download_tickers_control(driver, stocks, WAIT_TIME_FAST)
    _rm_crdownload(stocks, downloads)
    failed = _get_failed(stocks, downloads)
    failed_stocks = {x: stocks[x] for x in failed}
    print("DOWNLOAD TICKERS PART 2/3: ")
    _download_tickers_control(driver, failed_stocks, WAIT_TIME_SLOW1)
    _rm_crdownload(stocks, downloads)
    failed1 = _get_failed(failed_stocks, downloads)
    failed1_stocks = {x: failed_stocks[x] for x in failed1}
    print("DOWNLOAD TICKERS PART 3/3: ")
    _download_tickers_control(driver, failed1_stocks, WAIT_TIME_SLOW2)
    _rm_crdownload(stocks, downloads)
    return _get_failed(failed1_stocks, downloads)
