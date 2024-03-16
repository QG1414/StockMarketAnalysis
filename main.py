from dash import Dash,html,dcc, callback, Output, Input
import pandas as pd
import plotly_express as px
import dash_bootstrap_components as dbc
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')

external_stylesheets = [dbc.themes.CERULEAN]
app=Dash(__name__, external_stylesheets=external_stylesheets)

colors ={
    'background':'#19181A',
    'text':'#B19F9E'
}

app.layout=dbc.Container(style={'backgroundColor':colors['background'],'height':'100vh','overflow':'auto'},children=[
    dbc.Row([
         html.Div(
        children='Data Stock Analysis',
        className="text-primary text-center fs-3"
            )
    ]),
    dbc.Row([
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label':x,'value':x} for x in ['long','lat','cnt']
                ],
                value='long'
            )
        ]
    ),
       dbc.Row([
               dcc.Graph(figure={}, id='graph')
        ])
])
@callback(
    Output(component_id='graph',component_property='figure'),
    Input(component_id='dropdown',component_property='value')
)
def update_graph(col_chosen):
    figure= px.histogram(df,x='city',y=col_chosen)
    return figure

if __name__ == '__main__':
    app.run(debug=True)