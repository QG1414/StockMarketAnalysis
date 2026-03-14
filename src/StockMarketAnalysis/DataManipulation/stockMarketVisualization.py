import datetime
import logging
import os

import pandas as pd
import yfinance as yf
from Helpers.absolutePathGenerator import AbsolutePath

logger = logging.getLogger(__name__)


class StockMarketData:
    __base_data_name = AbsolutePath.resource_path(
        r"src\StockMarketAnalysis\DataManipulation\data\nasdaq_screener.csv"
    )
    __tickers_file_name = AbsolutePath.resource_path(
        r"src\StockMarketAnalysis\DataManipulation\data\YahooTickers.csv"
    )

    def __init__(self) -> None:
        if not os.path.exists(self.__tickers_file_name):
            self.create_tickers_file()
        self.__tickers_data = pd.read_csv(self.__tickers_file_name)
        self.__tickers_data["Symbol"] = self.__tickers_data["Symbol"].astype(str)

    def create_tickers_file(self) -> None:
        screener_data = pd.read_csv(self.__base_data_name)
        screener_data["Symbol"] = screener_data["Symbol"].astype(str)

        final_data = {"Symbol": [], "FullName": []}
        dataLength: int = len(screener_data["Symbol"].values)

        for index, key in enumerate(screener_data["Symbol"].values):
            try:
                stock = yf.Ticker(key)
                longName = stock.info["longName"]
                final_data["Symbol"] += [key]
                final_data["FullName"] += [longName]
                print(
                    f"TICKER {key}: {index}/{dataLength} COMPLETED: {round((float(index)/dataLength)*100,2): .2f}%"
                )
            except Exception as e:
                logger.critical(
                    f"Exception while importing data: {key} | Error message: {e}"
                )
                continue

        data_frame_to_save = pd.DataFrame(final_data)
        data_frame_to_save.reset_index(inplace=True, drop=True)
        data_frame_to_save.to_csv(
            self.__tickers_file_name, encoding="utf-8", index=False
        )

    def get_tickers(self) -> pd.DataFrame:
        return self.__tickers_data

    @staticmethod
    def get_company(
        ticker: str, startDate=None, endDate=datetime.datetime.now()
    ) -> pd.DataFrame:
        try:
            if startDate is None:
                company_data = yf.download(
                    tickers=ticker, threads=True, multi_level_index=False, period="max"
                )
            else:
                company_data = yf.download(
                    tickers=ticker,
                    threads=True,
                    start=startDate,
                    end=endDate,
                    multi_level_index=False,
                )
            company_data.reset_index(inplace=True)
        except Exception as e:
            logger.critical(
                f"Exception while downloading company {ticker} data | Error message: {e}"
            )
            return pd.DataFrame()
        return company_data

    @staticmethod
    def get_averages(companyData: pd.DataFrame) -> pd.DataFrame:
        companyData["MA10"] = (
            companyData["Close"].rolling(window=10).mean().reset_index(0, drop=True)
        )
        companyData["MA20"] = (
            companyData["Close"].rolling(window=20).mean().reset_index(0, drop=True)
        )
        return companyData

    @staticmethod
    def get_volatility(companyData: pd.DataFrame) -> pd.DataFrame:
        companyData["Volatility"] = (
            companyData["Close"]
            .pct_change()
            .rolling(window=10)
            .std()
            .reset_index(0, drop=True)
        )
        return companyData
