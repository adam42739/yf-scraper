from selenium.webdriver import Chrome
import datetime
import time

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


class Driver:

    def __init__(self):
        self._driver = Chrome()

    def __del__(self):
        self._driver.quit()

    def download_ticker(self, ticker, start_date, end_date, wait_time):
        url = _yahoo_url(ticker, start_date, end_date)
        self._driver.get(url)
        time.sleep(wait_time)
