import pandas as pd
import yfinance as yf
import os
from absolutePathGenerator import AbsolutePath


class StockMarketData:
    def __init__(self) -> None:
        self.__tickets_file_name = AbsolutePath.resource_path("dataScripts\\data\\YahooTickers.csv")
        self.__base_data_name = AbsolutePath.resource_path("dataScripts\\data\\nasdaq_screener.csv")

        if(not os.path.isfile(self.__tickets_file_name)):
            self.__create_tickets_file()
            
        self.__tickers_data = pd.read_csv(self.__tickets_file_name)

    def __create_tickets_file(self) -> None:
        screener_data = pd.read_csv(self.__base_data_name)
        screener_data["Symbol"] = screener_data["Symbol"].astype(str)

        final_data = {"Symbol":[],"FullName":[]}

        for i in screener_data["Symbol"].values:
            try:
                stock = yf.Ticker(i)
                longName = stock.info['longName']
                final_data["Symbol"] += [i]
                final_data["FullName"] += [longName]
            except:
                continue

        data_frame_to_save = pd.DataFrame(final_data)
        data_frame_to_save.reset_index(inplace=True, drop=True)
        data_frame_to_save.to_csv(self.__tickets_file_name, encoding="utf-8", index=False)
    
    def get_tickets(self) -> pd.DataFrame:
        return self.__tickers_data
    
    def get_company(self, ticket:str) -> pd.DataFrame:
        company_data = pd.DataFrame(yf.download(ticket))
        company_data.reset_index(inplace=True)
        return company_data