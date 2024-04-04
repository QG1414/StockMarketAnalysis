import plotly.graph_objects as go
import plotly_express as px
from dataScripts.stockMarketVisualization import StockMarketData
import pandas as pd
import numpy as np

class ChangeGraphs:
    @staticmethod
    def get_price_chart(current_company:pd.DataFrame,fullName : str):   
        figure = go.Figure()

        buyline, sellline = ChangeGraphs.linesBuySell(current_company['Close'])  # Pass 'Close' column to the function
        
        figure.add_trace(go.Scatter(x=current_company['Date'], y=buyline, mode='lines', line=dict(shape='spline', smoothing=0.1, color='red'),name='Buy Signal'))
        figure.add_trace(go.Scatter(x=current_company['Date'], y=sellline, mode='lines', line=dict(shape='spline', smoothing=0.1, color='green'),name='Sell Signal'))

        # Update layout
        figure.update_layout(template='plotly_dark', title=f'Stock Market Prices {fullName}', xaxis_title='Date', yaxis_title='Close Price')

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
    
    @staticmethod
    def linesBuySell(source):
        buyline = []
        sellline = []
        isBuy = False
        isSell = False
        start = len(source) - 3

        if source.iloc[start + 1] > source.iloc[start + 2]:
            buyline = source.iloc[-2:].tolist()
            sellline = [np.nan, np.nan]
        else:
            sellline = source.iloc[-2:].tolist()
            buyline = [np.nan, np.nan]

        for i in range(start, -1, -1):
            if not isBuy:
                isBuy = (source.iloc[i] > source.iloc[i + 1]) and (source.iloc[i + 1] < source.iloc[i + 2])
                if isBuy:
                    isSell = False

            if not isSell:
                isSell = (source.iloc[i] < source.iloc[i + 1]) and (source.iloc[i + 1] > source.iloc[i + 2])
                if isSell:
                    isBuy = False

            if not isBuy and not isSell:
                if(buyline[0] is not np.nan):
                    buyline.insert(0, source.iloc[i])
                else:
                    buyline.insert(0, np.nan)

                if sellline[0] is not np.nan:
                    sellline.insert(0, source.iloc[i])
                else:
                    sellline.insert(0,np.nan)

            if isBuy and not isSell:
                buyline.insert(0, source.iloc[i])
                if buyline[1] is not np.nan:
                    sellline.insert(0, np.nan)
                else:
                    sellline.insert(0, source.iloc[i])

            if isSell and not isBuy:
                sellline.insert(0, source.iloc[i])
                if sellline[1] is not np.nan:
                    buyline.insert(0, np.nan)
                else:
                    buyline.insert(0, source.iloc[i])

        return buyline, sellline

                                        
                                