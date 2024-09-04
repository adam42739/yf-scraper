# yf-scraper

## Introduction

yfscraper uses [Selenium](https://selenium-python.readthedocs.io) to scrape data from [yahoo finance](https://finance.yahoo.com).

## Installation

```python
pip install git+https://github.com/adam42739/yf-scraper.git#egg=yfscraper
```

## Usage

```python
import yfscraper as prices
```

### Downloading price data to a directory

```python
prices.download_data(tickers, downloads, base)
```

#### Parameters

> **`tickers`: _list_**

List of ticker to get pricing data for.

> **`downloads`: _str_**

Path to directory Chrome downloads files to.

> **`base`: _str_**

Path to directory where CSV files will be saved.

#### Returns

> **`failed`: _list_**

List of tickers yfscraper failed to get data for.

#### Example

```python
prices.download_data(["aapl", "msft"],"C:/Users/user1/Downloads/", "base/")
```

### Reading CSVs from the save directory

```python
prices.get_data(ticker, base)
```

#### Parameters

> **`ticker`: _str_**

Ticker for which to get the pricing data.

> **`base`: _str_**

Path to directory where CSV files are saved.

#### Returns

> **`df`: _pandas.DataFrame_**

Pricing data for the given ticker.

#### Example

```python
prices.get_data("aapl", "base/")
```

Output:

```console
         Date      Open      High       Low     Close  Adj Close     Volume
0  1980-12-12  0.128348  0.128906  0.128348  0.128348   0.098943  469033600
```

### Getting metadata

```python
prices.get_metadata(base)
```

#### Parameters

> **`base`: _str_**

Path to directory where CSV files are saved.

#### Returns

> **`data`: _dict_**

Metadata for the stocks stores in `base`.

#### Example

```python
prices.get_metadata("base/")
```

Output:

```console
{
    "aapl": 2024-09-04 00:00:00,
    "amzn": 2024-09-04 00:00:00
}
```
