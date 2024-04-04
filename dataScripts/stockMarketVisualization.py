import pandas as pd
import yfinance as yf
import os
from absolutePathGenerator import AbsolutePath
import datetime


class StockMarketData:
    def __init__(self) -> None:
        __tickets_url = "https://drive.google.com/file/d/1sl0pmPgA3FISpp28KoYqqiFfG46DvMVX/view?usp=sharing"
        __tickets_url = 'https://drive.google.com/uc?id=' + __tickets_url.split('/')[-2]
            
        self.__tickers_data = pd.read_csv(__tickets_url)
        self.__tickers_data["Symbol"] = self.__tickers_data["Symbol"].astype(str)

    # def __create_tickets_file(self) -> None:
    #     screener_data = pd.read_csv(self.__base_data_name)
    #     screener_data["Symbol"] = screener_data["Symbol"].astype(str)

    #     final_data = {"Symbol":[],"FullName":[]}

    #     for i in screener_data["Symbol"].values:
    #         try:
    #             stock = yf.Ticker(i)
    #             longName = stock.info['longName']
    #             final_data["Symbol"] += [i]
    #             final_data["FullName"] += [longName]
    #         except:
    #             continue

    #     data_frame_to_save = pd.DataFrame(final_data)
    #     data_frame_to_save.reset_index(inplace=True, drop=True)
    #     data_frame_to_save.to_csv(self.__tickets_file_name, encoding="utf-8", index=False)
    
    def get_tickets(self) -> pd.DataFrame:
        return self.__tickers_data
    
    @staticmethod
    def get_company(ticket:str, startDate = None, endDate=datetime.datetime.now()) -> pd.DataFrame:
        try:
            if startDate == None:
                company_data = yf.download(tickers=ticket, threads=True)
            else:
                company_data = yf.download(tickers=ticket, threads=True, start=startDate, end=endDate)
            company_data.reset_index(inplace=True)
        except:
            return pd.DataFrame()
        return company_data
    
    @staticmethod
    def get_averages(companyData:pd.DataFrame) -> pd.DataFrame:
        companyData['MA10'] = companyData['Close'].rolling(window=10).mean().reset_index(0, drop=True)
        companyData['MA20'] = companyData['Close'].rolling(window=20).mean().reset_index(0, drop=True)
        return companyData
    
    @staticmethod
    def get_volatility(companyData:pd.DataFrame) -> pd.DataFrame:
        companyData['Volatility'] = companyData['Close'].pct_change().rolling(window=10).std().reset_index(0, drop=True)
        return companyData