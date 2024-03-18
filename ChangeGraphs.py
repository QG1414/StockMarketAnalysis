import plotly_express as px
from dataScripts.stockMarketVisualization import StockMarketData
class ChangeGraphs:
    def __init__(self, df):
        self.df = df
    def changeGraphToBox(self, col_chosen, fullName : str):
        col_chosen = StockMarketData.get_averages(col_chosen)
        figure= px.line(col_chosen,x='Date',y=["Close","MA10","MA20"],template= 'plotly_dark',title=f'Moving Averages{fullName}')
        figure.update_layout(
            font_family='Courier New',
            font_size=13,
            title_font_family="Times New Roman",
            title_font_size=20,
            xaxis=dict(
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
                            label="YTD",
                            step="year",
                            stepmode="backward"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(count=3,
                            label="3y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=False
                ),
                type="date"
            )
        )
        return figure
    def changeGraphToHistogram(self, col_chosen,fullName : str):
        col_chosen = StockMarketData.get_volatility(col_chosen)
        figure= px.line(col_chosen,x="Date",y="Volatility",template= 'plotly_dark',title=f'Volatility{fullName}')
        figure.update_layout(
            font_family='Courier New',
            font_size=13,
            title_font_family="Times New Roman",
            title_font_size=20
        )
        return figure