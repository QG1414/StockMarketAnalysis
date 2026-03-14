import logging

import dash_bootstrap_components as dbc
import plotly.io as pio
from dash import Dash
from DataManipulation.stockMarketVisualization import StockMarketData
from Helpers.absolutePathGenerator import AbsolutePath
from Layout.Callbacks.callbacks import Callbacks
from Layout.layout import Layout

logger = logging.getLogger(__name__)

pio.templates.default = "plotly_dark"
external_stylesheets = [dbc.themes.CERULEAN]

__app = Dash(__name__, external_stylesheets=external_stylesheets)
server = __app.server


class MainApp:
    def __init__(self, app) -> None:
        logging.basicConfig(
            filename=AbsolutePath.resource_path(r"logs\StockAnalysis.log"),
            encoding="utf-8",
            level=logging.DEBUG,
        )
        self.__app = app
        self.__market_object = StockMarketData()
        self.__df_tickers = self.__market_object.get_tickers()
        self.__layout_data = Layout(self.__df_tickers)

        self.__callbacks = Callbacks()
        self.__callbacks.get_callbacks(self.__app, self.__layout_data)

        self.__app.layout = self.__on_page_reload

    def run_app(self) -> None:
        self.__app.run()

    def __on_page_reload(self):
        self.__callbacks.reset_values()
        return self.__layout_data.content_layout


app = MainApp(__app)


if __name__ == "__main__":
    app.run_app()
