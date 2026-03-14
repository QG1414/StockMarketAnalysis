# Stock Market Analysis

Authors: Kacper Potaczała & [Łukasz Cal](https://github.com/luszekpog)

## Basic Info

This application calculates and visualizes multiple market indicators for over 4000 NASDAQ stocks.

* Information about indicators is listed [here](#indicators)
* Installation instructions are explained [here](#installation)
* Usage instructions are explained [here](#usage)
* Known bugs are listed [here](#known-bugs)

## Indicators

There are four different charts in total, and each chart can display multiple indicators.

* **Stock Price Chart & Buy/Sell Signal** – Used to indicate potential buy or sell opportunities based on the calculated indicators.
* **Moving Averages Chart** – Used to smooth price data and help identify market trends.
* **Volatility Chart** – Shows the level of price fluctuations, helping to assess market volatility and risk.
* **Correlation Chart** – Shows the linear correlation between two selected stocks.

## Installation

To install the application, simply clone the repository:

```
git clone https://github.com/QG1414/StockMarketAnalysis.git
```

Then create a virtual environment and activate it using the terminal, for example:

```
python -m venv .venv
.\.venv\Scripts\activate
```

Install all requirements listed in [this file](https://github.com/QG1414/StockMarketAnalysis/blob/main/requirements.txt):

```
pip install -r .\requirements.txt
```

## Usage

To start the application, run the following command while the virtual environment is active:

```
python .\src\StockMarketAnalysis\main.py
```

You should then see a line in the terminal:

**Dash is running on http://127.0.0.1:8050/**
(The URL may be different for different users.)

Copy and paste this link into your browser.

The page is divided into two sections:

* **Stock Price & Buy/Sell Signal, Moving Averages, and Volatility**
* **Correlation**

Each section contains a dropdown with all available stocks. It is recommended to use the text search instead of scrolling through the entire list.

The first section has only one dropdown. After selecting a stock, wait a few seconds for the data to load.

The first chart also contains a time range selector in the bottom-right corner that allows you to view data from different time periods:

* 1d – 1 day
* 1w – 1 week
* 1m – 1 month
* 3m – 3 months
* 6m – 6 months
* 1y – 1 year
* 3y – 3 years
* all – all available data

Note that **all** may be shorter than **3y** if the stock is relatively new.

To switch from the default **Stock Price & Buy/Sell Signal** chart, click the button in the top-right corner labeled **"Change graph"**.

Charts change cyclically:

Stock Price & Buy/Sell Signal → Moving Averages → Volatility → Stock Price & Buy/Sell Signal → ...

The second section contains two dropdowns used to check the correlation between two companies.

Only scatter plot points and a regression line are displayed. The regression line is linear.

## Known Bugs

* Selecting the same stock for both inputs in the correlation chart causes an error and displays no results.
* Slow data loading.

## Notes

* The first version of this application was hosted online, but it is currently accessible only from a local network.
