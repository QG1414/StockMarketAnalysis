import plotly_express as px
from dataScripts.stockMarketVisualization import StockMarketData
class ChangeGraphs:
    def __init__(self, df):
        self.df = df
    def changeGraphToBox(self, col_chosen, fullName : str):
        figure= px.line(col_chosen,x='Date',y=["Close","MA10","MA20"],template= 'plotly_dark',title=f'Moving Averages{fullName}')
        figure.update_layout(
            font_family='Courier New',
            font_size=13,
            title_font_family="Times New Roman",
            title_font_size=20
        )
        return figure
    def changeGraphToHistogram(self, col_chosen,fullName : str):
        figure= px.line(col_chosen,x="Date",y="Volatility",template= 'plotly_dark',title=f'Volatility{fullName}')
        figure.update_layout(
            font_family='Courier New',
            font_size=13,
            title_font_family="Times New Roman",
            title_font_size=20
        )
        return figure