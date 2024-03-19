from dash import Dash,html,dcc, callback, Output, Input, ctx, State
from dash.exceptions import PreventUpdate
import plotly_express as px
import dash_bootstrap_components as dbc
from ChangeGraphs import ChangeGraphs
from dataScripts.stockMarketVisualization import StockMarketData
from correlationGraph import CorrelationGraph
import plotly.io as pio
import pandas as pd
from datetime import datetime

pio.templates.default = "plotly_dark"
external_stylesheets = [dbc.themes.CERULEAN]
app=Dash(__name__, external_stylesheets=external_stylesheets)

market_object = StockMarketData()
df_tickers = market_object.get_tickets()

lastTicket = ""
current_company = pd.DataFrame()
current_avarages = None
current_volatility = None

c=0
colors ={
    'bg':'#111111',
    'text':'#FFFFFF',
    'text2':'#AAAAAA',
    'chart':'#7B5668',
    'chart2':'#3E5077'
}


app.layout=dbc.Container(children=[
    dbc.Row([
         html.Div(
        children='Data Stock Analysis📊',
        className="font-weight-bold text-center display-2 p-3",
        style={
            'color': colors['text'],
            'background-color': colors['bg']
        }
            )
    ]),
    dbc.Row([
        html.Hr(
            style={
                'color': colors['text']
            }
        )
    ]),
    dbc.Row([
            dcc.Dropdown(
                df_tickers["Symbol"] + " - " + df_tickers["FullName"],
                id='dropdown',
                className='pt-5 w-25 mx-auto',
                style={'background-color': colors['bg'],'color': colors["text2"]}
            )
        ],
        style={"margin-bottom": "20px"}
    ),
        
        dbc.Row([
              dbc.Button("Change graph", id="change_graph_button",color=colors['bg'], className="m-4 me-1 border border-white rounded ",style={'color': colors['text'],'width':'120px', 'font-size':'13px'},n_clicks=0),
        ],className="w-100 d-flex flex-row-reverse"),
       dbc.Row([
               dcc.Graph( id='graph',figure={"layout":{
                   "template":"plotly_dark",
                   'overflowX': 'scroll'
               }})
        ]),
    
        dbc.Row([
        html.Hr(
            style={
                'color': colors['text'],
                'margin-top':'20px'
            }
        )
        ]),
        dbc.Row([
            html.Div(
            children='Correlation beetwen companies',
            className="font-weight-bold text-center display-6 p-3 pt-5",
            style={
                'color': colors['text'],
                'background-color': colors['bg']
            }
                )
        ]),
        dbc.Row([
            dbc.Col(
            dcc.Dropdown(
                df_tickers["Symbol"] + " - " + df_tickers["FullName"],
                id='correlation_dropdown',
                className='pt-5 w-50 mx-auto',
                style={'background-color': colors['bg'],'color': colors["text2"]}
            )
            ),
            dbc.Col(
            dcc.Dropdown(
                df_tickers["Symbol"] + " - " + df_tickers["FullName"],
                id='correlation2_dropdown',
                className='pt-5 w-50 mx-auto',
                style={'background-color': colors['bg'],'color': colors["text2"]}
            )
            )
        ],
        style={"margin-bottom": "20px"}
    ),
     dbc.Row([
               dcc.Graph( id='corr_graph',figure={"layout":{
                   "template":"plotly_dark"
               }})
        ]),
         dbc.Row(
            dbc.Col(
            html.P(
                f"\u00A9 All rights reserved. Made by Kacper Potaczała and Łukasz Cal.",
                className="text-end text-white pt-3",
            ),
            width={"size": 12},
            style={"background-color": "#2E3135"}
            )
        )


],fluid=True,style={'background-color': colors['bg'],'overflow': 'auto','height':'100vh'})
@callback(
    Output(component_id="graph", component_property='figure', allow_duplicate=True),
    Input(component_id='dropdown',component_property='value'),
    Input(component_id='change_graph_button',component_property='n_clicks'),
    prevent_initial_call=True
)
def update_graph(company_choosen : str,n):
    global lastTicket
    global current_company
    global current_avarages
    global current_volatility
    
    if company_choosen == None:
        return px.line(template= 'plotly_dark')

    cg = ChangeGraphs(df_tickers)
    ticket = company_choosen.split("-")[0]

    if ticket != lastTicket:
        lastTicket = ticket
        company_fetched = market_object.get_company(lastTicket)
        if company_fetched.empty:
            lastTicket = ""
            return px.line(template= 'plotly_dark')
        current_company = company_fetched
        current_avarages = market_object.get_averages(current_company)
        current_volatility = market_object.get_volatility(current_company)
    
    textSplited = company_choosen.split("-")
    companyName = f"<br>{textSplited[0]} - ({textSplited[1].strip()})"
    global c
    if ctx.triggered_id=='change_graph_button': c = c+1
    if c>2:
        c=0
        
    if c==0:
        figure= px.line(current_company,x='Date',y="Close",template= 'plotly_dark',title=f'Stock Market Prices{companyName}')
    elif c==1:
        figure = cg.changeGraphToBox(current_avarages, companyName)
    else:
        figure = cg.changeGraphToHistogram(current_volatility,companyName)
    
    figure.update_layout(
            xaxis=None
    )
    
    figure.update_layout(
            font_family='Courier New',
            font_size=13,
            title_font_family="Times New Roman",
            title_font_size=20,
            xaxis=cg.getRangeselectors()
    )
    
    return figure
    
@callback(
    Output(component_id='corr_graph',component_property='figure'),
    Input(component_id='correlation_dropdown',component_property='value'),
    Input(component_id='correlation2_dropdown',component_property='value')
)
def getCorrelationGrap(company1,company2):
    if company1 == None or company2 == None:
        return px.scatter(template= 'plotly_dark')
    
    company_fetched1 = market_object.get_company(company1.split("-")[0], startDate=(datetime.now() - pd.DateOffset(years=1)))
    textSplited1 = company1.split("-")
    company_fetched2 = market_object.get_company(company2.split("-")[0], startDate=(datetime.now() - pd.DateOffset(years=1)))     
    
    if company_fetched1.empty or company_fetched2.empty:
        return px.scatter(template= 'plotly_dark')
     
    textSplited2 = company2.split("-")                                     
    corrg = CorrelationGraph(df_tickers)
    fig = corrg.handleCorrelation(company_fetched1,company_fetched2,textSplited1,textSplited2)
    return fig

@app.callback(
    Output(component_id = "graph", component_property="figure",),
    Input(component_id= "graph", component_property="relayoutData"),
    State(component_id="graph",component_property= "figure"),
    Input(component_id='dropdown',component_property='value'),
)
def update_figure(relayout_data, fig, company_choosen):
    global current_company
    global current_avarages
    global current_volatility
    global c
    
    if company_choosen == None:
        return px.line(template= 'plotly_dark')

    if current_company.empty:
        raise PreventUpdate

    if (relayout_data is None) or ("xaxis.range[0]" not in relayout_data):
        fig["layout"]["yaxis"]["autorange"] = True
        return fig
    
    mask = (current_company['Date'] >= pd.Timestamp(relayout_data["xaxis.range[0]"])) & (current_company['Date'] <= pd.Timestamp(relayout_data["xaxis.range[1]"]))

    in_view = pd.DataFrame()

    if c==0:
        in_view = current_company.loc[mask]
        minValue = in_view.min()["Close"]
        maxValue = in_view.max()["Close"]
    elif c==1:
        in_view = market_object.get_averages(current_company)
        in_view = in_view[mask]
        minValue = min(in_view.min()["Close"], in_view.min()["MA10"], in_view.min()["MA20"])
        maxValue = max(in_view.max()["Close"], in_view.max()["MA10"], in_view.max()["MA20"])
    else:
        in_view = market_object.get_volatility(current_company)
        in_view = in_view[mask]
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

if __name__ == '__main__':
    app.run(debug=True)