import requests
import pandas
import datetime
import io
import time
import random

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
        + ticker
        + YAHOO_LINK2
        + str(_yahoo_date_number(start_date))
        + YAHOO_LINK3
        + str(_yahoo_date_number(end_date))
    )


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
    url = _yahoo_url(ticker, start_date, end_date)
    time.sleep(random.randint(15, 30))
    text = requests.get(url, headers=headers).text
    df = pandas.read_html(io.StringIO(text))
    df = df[0]
    df = df.rename(COLS, axis="columns")
    df["Open"] = df["Open"].astype(str)
    df = df[~df["Open"].str.contains("[a-zA-Z]")]
    df["Open"] = df["Open"].astype(float)
    df["Date"] = pandas.to_datetime(df["Date"], format="%b %d, %Y")
    if "Date" in df:
        return df[list(COLS.values())]
    else:
        return pandas.DataFrame()
