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


def _yahoo_url(ticker):
    return (
        YAHOO_LINK1
        + _yahoo_ticker_format(ticker)
        + YAHOO_LINK2
        + str(_yahoo_date_number(YAHOO_START_DATE))
        + YAHOO_LINK3
        + str(_yahoo_date_number(datetime.datetime.today()))
        + YAHOO_LINK4
    )


def _yahoo_ticker_format(ticker):
    return ticker.upper().replace(".", "-")


class _Driver:

    def __init__(self):
        self._driver = Chrome()

    def __del__(self):
        self._driver.quit()

    def download_ticker(self, ticker, wait_time):
        url = _yahoo_url(ticker)
        self._driver.get(url)
        time.sleep(wait_time)


def _download_tickers_control(driver, tickers, wait_time):
    for ticker in tqdm.tqdm(tickers):
        driver.download_ticker(ticker, wait_time)


def _rm_crdownload(tickers, downloads):
    for ticker in tickers:
        path = downloads + _yahoo_ticker_format(ticker) + ".crdownload"
        if os.path.exists(path):
            os.remove(path)


def download_ticker_path(ticker, downloads):
    return downloads + _yahoo_ticker_format(ticker) + ".csv"


def _exists(ticker, downloads):
    return os.path.exists(download_ticker_path(ticker, downloads))


def _get_failed(tickers, downloads):
    failed = []
    for ticker in tickers:
        if not _exists(ticker, downloads):
            failed.append(ticker)
    return failed


WAIT_TIME_FAST = 0.3
WAIT_TIME_SLOW1 = 1
WAIT_TIME_SLOW2 = 5


def download_tickers(tickers, downloads):
    driver = _Driver()
    print("DOWNLOAD TICKERS PART 1/3: ")
    _download_tickers_control(driver, tickers, WAIT_TIME_FAST)
    _rm_crdownload(tickers, downloads)
    failed = _get_failed(tickers, downloads)
    print("DOWNLOAD TICKERS PART 2/3: ")
    _download_tickers_control(driver, failed, WAIT_TIME_SLOW1)
    _rm_crdownload(failed, downloads)
    failed1 = _get_failed(failed, downloads)
    print("DOWNLOAD TICKERS PART 3/3: ")
    _download_tickers_control(driver, failed1, WAIT_TIME_SLOW2)
    _rm_crdownload(failed1, downloads)
    return _get_failed(failed1, downloads)
