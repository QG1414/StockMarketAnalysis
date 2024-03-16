from dash import Dash,html,dcc, callback, Output, Input
import pandas as pd
import plotly_express as px
import dash_bootstrap_components as dbc
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')

external_stylesheets = [dbc.themes.CERULEAN]
app=Dash(__name__, external_stylesheets=external_stylesheets)

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
                id='dropdown',
                options=[
                    {'label': html.Span(x,style={'color': colors['text2']}),'value':x} for x in ['long','lat','cnt']
                ],
                value='long',
                className='pt-5 w-25 mx-auto',
                style={'background-color': colors['bg'],'color': colors['text']}
            )
        ]
    ),
       dbc.Row([
               dcc.Graph( id='graph',figure={})
        ])
],fluid=True,style={'background-color': colors['bg'],'overflow': 'auto','height':'100vh'})
@callback(
    Output(component_id='graph',component_property='figure'),
    Input(component_id='dropdown',component_property='value')
)
def update_graph(col_chosen):
    figure= px.bar(df,x='city',y=col_chosen,color='city',template= 'plotly_dark',title='place for chart title')
    figure.update_layout(
        font_family='Courier New',
        font_size=13,
        title_font_family="Times New Roman",
        title_font_size=20
    )
    return figure

if __name__ == '__main__':
    app.run(debug=True)