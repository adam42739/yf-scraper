import requests
import pandas
import datetime

YAHOO_START_DATE = datetime.datetime(1970, 1, 1)
YAHOO_DATE_ITER = 86400


def _yahoo_date_number(date):
    return (date - YAHOO_START_DATE).days * YAHOO_DATE_ITER


YAHOO_LINK1 = "https://finance.yahoo.com/quote/"
YAHOO_LINK2 = "/history/?period1="
YAHOO_LINK3 = "&period2="


def _yahoo_url(ticker, start_date, end_date):
    return (
        YAHOO_LINK1
        + _yahoo_ticker_format(ticker)
        + YAHOO_LINK2
        + str(_yahoo_date_number(start_date))
        + YAHOO_LINK3
        + str(_yahoo_date_number(end_date))
    )


def _yahoo_ticker_format(ticker):
    return ticker.upper().replace(".", "-")


COLS = {
    "Date": "Date",
    "Open": "Open",
    "High": "High",
    "Low": "Low",
    "Close Close price adjusted for splits.": "Close",
    "Adj Close Adjusted close price adjusted for splits and dividend and/or capital gain distributions.": "Adj Close",
    "Volume": "Volume",
}


def get_price_df(ticker, start_date, end_date):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = _yahoo_url(_yahoo_ticker_format(ticker), start_date, end_date)
    text = requests.get(url, headers=headers).text
    df = pandas.read_html(text)
    df = df[0]
    df = df.rename(COLS, axis="columns")
    df = df[["Date", "Open", "High", "Low", "Close"]]
    print(df.head())


START_DATE = datetime.datetime(2020, 1, 1)
END_DATE = datetime.datetime(2021, 1, 1)


get_price_df("aapl", START_DATE, END_DATE)

a = 0
