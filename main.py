from dash import Dash,html,dcc, callback, Output, Input, ctx
import plotly_express as px
import dash_bootstrap_components as dbc
from ChangeGraphs import ChangeGraphs
from dataScripts.stockMarketVisualization import StockMarketData
from correlationGraph import CorrelationGraph
import plotly.io as pio


pio.templates.default = "plotly_dark"
external_stylesheets = [dbc.themes.CERULEAN]
app=Dash(__name__, external_stylesheets=external_stylesheets)

market_object = StockMarketData()
df_tickers = market_object.get_tickets()

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
                value='A - "Agilent Technologies, Inc."',
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
                   "template":"plotly_dark"
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
                value='MSFT - "Microsoft Corporation"',
                className='pt-5 w-25 mx-auto',
                style={'background-color': colors['bg'],'color': colors["text2"]}
            )
            ),
            dbc.Col(
            dcc.Dropdown(
                df_tickers["Symbol"] + " - " + df_tickers["FullName"],
                id='correlation2_dropdown',
                value='AAPL - "Apple, Inc."',
                className='pt-5 w-25 mx-auto',
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
    Output(component_id='graph',component_property='figure'),
    Input(component_id='dropdown',component_property='value'),
    Input(component_id='change_graph_button',component_property='n_clicks')
)

def update_graph(company_choosen : str,n):
    if company_choosen == None:
        return px.line(template= 'plotly_dark')

    cg = ChangeGraphs(df_tickers)
    company_fetched = market_object.get_company(company_choosen.split("-")[0])
    textSplited = company_choosen.split("-")
    companyName = f"<br>{textSplited[0]} - ({textSplited[1].strip()})"
    global c
    if ctx.triggered_id=='change_graph_button': c = c+1
    if c>2:
        c=0
    if c==0:
        figure= px.line(company_fetched,x='Date',y="Close",template= 'plotly_dark',title=f'Stock Market Prices{companyName}')
        figure.update_layout(
            font_family='Courier New',
            font_size=13,
            title_font_family="Times New Roman",
            title_font_size=20
        )
        return figure
    elif c==1:
        figure = cg.changeGraphToBox(company_fetched, companyName)
        return figure
    elif c==2:
        figure = cg.changeGraphToHistogram(company_fetched,companyName)
        return figure
    
@callback(
    Output(component_id='corr_graph',component_property='figure'),
    Input(component_id='correlation_dropdown',component_property='value'),
    Input(component_id='correlation2_dropdown',component_property='value')
)
def getCorrelationGrap(company1,company2):
    company_fetched1 = market_object.get_company(company1.split("-")[0])
    textSplited1 = company1.split("-")
    company_fetched2 = market_object.get_company(company2.split("-")[0])      
    textSplited2 = company2.split("-")                                     
    corrg = CorrelationGraph(df_tickers)
    fig = corrg.handleCorrelation(company_fetched1,company_fetched2,textSplited1,textSplited2)
    return fig
    

if __name__ == '__main__':
    app.run(debug=True)