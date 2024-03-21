import plotly_express as px
from dataScripts.stockMarketVisualization import StockMarketData
import pandas as pd

class ChangeGraphs:
    @staticmethod
    def get_price_chart(current_company:pd.DataFrame,fullName : str):
        figure= px.line(current_company,x='Date',y="Close",template= 'plotly_dark',title=f'Stock Market Prices{fullName}')
        return figure
    
    @staticmethod
    def get_avarages_chart(current_company:pd.DataFrame, fullName : str):
        figure= px.line(current_company,x='Date',y=["Close","MA10","MA20"],template= 'plotly_dark',title=f'Moving Avarages{fullName}')
        return figure
    
    @staticmethod
    def get_volatility_chart(current_company:pd.DataFrame,fullName : str):
        figure= px.line(current_company,x="Date",y="Volatility",template= 'plotly_dark',title=f'Volatility{fullName}')
        return figure
    
    @staticmethod
    def getRangeselectors() -> dict:
        dictionaryToReturn = dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1d",
                            step="day",
                            stepmode="backward"),
                        dict(count=7,
                            label="1w",
                            step="day",
                            stepmode="backward"),
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=3,
                            label="3m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(count=3,
                            label="3y",
                            step="year",
                            stepmode="backward"
                            ),
                        dict(step="all")
                    ]),
                    y=-0.25,
                    x=1,
                    yanchor = "auto",
                    xanchor="auto",
                    borderwidth=1,
                    font=dict(
                        color="white",
                        size=20
                    ),
                    bgcolor="#322485"
                ),
                rangeslider=dict(
                    visible=False
                ),
                type="date"
            )
        
        return dictionaryToReturn