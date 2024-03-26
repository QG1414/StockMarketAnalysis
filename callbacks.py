from dash import Dash,callback, Output, Input, State
from dataScripts.stockMarketVisualization import StockMarketData
import plotly_express as px
from ChangeGraphs import ChangeGraphs
from correlationGraph import CorrelationGraph
from datetime import datetime
import pandas as pd


class Callbacks:
    def __init__(self) -> None:
        self.reset_values()

    def reset_values(self):
        self.__lastTicket = ""
        self.__current_company = pd.DataFrame()


    def get_callbacks(self,app:Dash, df_tickers:pd.DataFrame) -> None:
        @callback(
            Output(component_id="graph", component_property='figure',allow_duplicate=True),
            Output(component_id='change_graph_button',component_property='n_clicks',allow_duplicate=True),
            Input(component_id='dropdown',component_property='value'),
            State(component_id='change_graph_button',component_property='n_clicks'),
            prevent_initial_call=True
        )
        def new_company_graph(company_choosen : str, n:int):
            if company_choosen == None:
                self.__lastTicket = ""
                return px.line(template= 'plotly_dark'),n-1

            ticket = company_choosen.split("-")[0]

            self.__lastTicket = ticket
            company_fetched = StockMarketData.get_company(self.__lastTicket)
            if company_fetched.empty:
                self.__lastTicket = ""
                return px.line(template= 'plotly_dark'),n-1
            
            self.__current_company = company_fetched

            return update_graph(company_choosen,n)
        
        @callback(
            Output(component_id="graph", component_property='figure',allow_duplicate=True),
            Output(component_id='change_graph_button',component_property='n_clicks',allow_duplicate=True),
            State(component_id='dropdown',component_property='value'),
            Input(component_id='change_graph_button',component_property='n_clicks'),
            prevent_initial_call=True
        )
        def update_graph(company_choosen:str,n:int):     
            if len(self.__lastTicket) == 0:
                return px.line(template= 'plotly_dark'), n-1
            
            textSplited = company_choosen.split("-")
            companyName = f"<br>{textSplited[0]} - ({textSplited[1].strip()})"
                
            if n % 3 == 0:
                figure = ChangeGraphs.get_price_chart(self.__current_company, companyName)
            elif n % 3 == 1:
                figure = ChangeGraphs.get_avarages_chart(StockMarketData.get_averages(self.__current_company), companyName)
            else:
                figure = ChangeGraphs.get_volatility_chart(StockMarketData.get_volatility(self.__current_company),companyName)
            

            figure.update_layout(
                    font_family='Courier New',
                    font_size=13,
                    title_font_family="Times New Roman",
                    title_font_size=20,
                    xaxis=ChangeGraphs.getRangeselectors()
            )


            return figure, n
        


        @callback(
            Output(component_id='corr_graph',component_property='figure'),
            Input(component_id='correlation_dropdown',component_property='value'),
            Input(component_id='correlation2_dropdown',component_property='value')
        )
        def getCorrelationGraph(company1,company2):
            if company1 == None or company2 == None:
                return px.scatter(template= 'plotly_dark')
            
            company_fetched1 = StockMarketData.get_company(company1.split("-")[0], startDate=(datetime.now() - pd.DateOffset(years=1)))
            textSplited1 = company1.split("-")
            company_fetched2 = StockMarketData.get_company(company2.split("-")[0], startDate=(datetime.now() - pd.DateOffset(years=1)))     
            
            if company_fetched1.empty or company_fetched2.empty:
                return px.scatter(template= 'plotly_dark')
            
            textSplited2 = company2.split("-")                                     
            corrg = CorrelationGraph(df_tickers)
            fig = corrg.handleCorrelation(company_fetched1,company_fetched2,textSplited1,textSplited2)
            return fig



        @app.callback(
            Output(component_id = "graph", component_property="figure",allow_duplicate=True),
            Input(component_id= "graph", component_property="relayoutData"),
            State(component_id="graph",component_property= "figure"),
            State(component_id='change_graph_button',component_property='n_clicks'),
            prevent_initial_call=True
        )
        def update_figure(relayout_data, fig, n):
            if self.__current_company.empty:
                return px.line(template= 'plotly_dark')

            if (relayout_data is None) or ("xaxis.range[0]" not in relayout_data):
                fig["layout"]["yaxis"]["autorange"] = True
                return fig

            mask = (self.__current_company['Date'] >= pd.Timestamp(relayout_data["xaxis.range[0]"])) & (self.__current_company['Date'] <= pd.Timestamp(relayout_data["xaxis.range[1]"]))

            in_view = pd.DataFrame()

            if n%3==0:
                in_view = self.__current_company.loc[mask]
                minValue = in_view.min()["Close"]
                maxValue = in_view.max()["Close"]
            elif n%3==1:
                current_avarages = StockMarketData.get_averages(self.__current_company)
                in_view = current_avarages.loc[mask]
                minValue = min(in_view.min()["Close"], in_view.min()["MA10"], in_view.min()["MA20"])
                maxValue = max(in_view.max()["Close"], in_view.max()["MA10"], in_view.max()["MA20"])
            else:
                current_volatility = StockMarketData.get_volatility(self.__current_company)
                in_view = current_volatility.loc[mask]
                minValue = in_view.min()["Volatility"]
                maxValue = in_view.max()["Volatility"] 
            
            difference = (maxValue - minValue) / 5
            maxValue += difference
            minValue -= difference
            if minValue < 0:
                minValue = 0

            
            fig["layout"]["yaxis"]["autorange"] = False
            fig["layout"]["yaxis"]["range"] = [
                minValue,
                maxValue,
            ]

            return fig