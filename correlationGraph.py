import plotly_express as px
import pandas as pd
from dataScripts.stockMarketVisualization import StockMarketData
class CorrelationGraph(object):
    def __init__(self, df):
        self.df = df
    
    def handleCorrelation(self, chosen1, chosen2,c_name1,c_name2):
        company1 = StockMarketData.get_averages(chosen1)
        company1_value = company1.loc[:,['Date', 'Close']]
        company2 = StockMarketData.get_averages(chosen2)
        company2_value = company2.loc[:,['Date', 'Close']]
        chosen = pd.merge(company1_value,company2_value, on='Date')
        chosen.rename(columns = {'Close_x':f'{c_name1[0]}','Close_y':f'{c_name2[0]}'}, inplace = True)

        fig = px.scatter(chosen, x=str(c_name1[0]), y=str(c_name2[0]), trendline="ols",title=f"Correlation between {c_name1[1]} and {c_name2[1]}")
        return fig