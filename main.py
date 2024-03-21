from dash import Dash
import dash_bootstrap_components as dbc
from dataScripts.stockMarketVisualization import StockMarketData
import plotly.io as pio
from layout import Layout
from callbacks import get_callbacks

pio.templates.default = "plotly_dark"
external_stylesheets = [dbc.themes.CERULEAN]

app=Dash(__name__, external_stylesheets=external_stylesheets)

market_object = StockMarketData()
df_tickers = market_object.get_tickets()

layout_data = Layout(df_tickers)

app.layout=layout_data.content_layout

get_callbacks(app,df_tickers)



if __name__ == '__main__':
    app.run(debug=True)