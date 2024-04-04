from dash import html,dcc
import dash_bootstrap_components as dbc
import pandas as pd

class Layout:
    def __init__(self, df_tickers : pd.DataFrame) -> None:
        self.colors ={
            'bg':'#111111',
            'text':'#FFFFFF',
            'text2':'#AAAAAA',
            'chart':'#7B5668',
            'chart2':'#3E5077'
        }
        self.df_tickers = df_tickers
        self.content_layout = self.__get_layout()

    def __get_layout(self) -> dbc.Container:
        content_layout = dbc.Container(children=[
            dbc.Row([
                html.Div(
                    children=[
                    html.P(
                        children='Data Stock Analysis',
                        className="font-weight-bold text-center",
                        style={
                            'color': self.colors['text'],
                            'display': 'inline-block'
                            # 'background-color': self.colors['bg']
                        },
                    ),
                    html.Img(
                        src="https://drive.google.com/thumbnail?id=" + "https://drive.google.com/file/d/1vtkE87R6gG-RCqaUnK5WeKLSYusAlAme/view?usp=sharing".split('/')[-2],
                        className="img-fluid",
                        style={
                            "width":"7%",
                            'display': 'inline-block'
                        }
                    )
                ],
                className="font-weight-bold text-center display-2 p-3",
                style={
                    'background-image': 'linear-gradient(#152559 1%, #111111 49%)'
                }

                )
            ]),
            # dbc.Row([
            #     html.Hr(
            #         style={
            #             'color': self.colors['text']
            #         }
            #     )
            # ]),
            dbc.Row([
                    dcc.Dropdown(
                        self.df_tickers["Symbol"] + " - " + self.df_tickers["FullName"],
                        id='dropdown',
                        className='pt-5 w-25 mx-auto',
                        style={'background-color': self.colors['bg'],'color': self.colors["text2"]}
                    )
                ],
                style={"margin-bottom": "20px"}
            ),
                
                dbc.Row([
                    dbc.Button("Change graph", id="change_graph_button",color=self.colors['bg'], className="m-4 me-1 border border-white rounded ",style={'color': self.colors['text'],'width':'120px', 'font-size':'13px'},n_clicks=0),
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
                        'color': self.colors['text'],
                        'margin-top':'20px'
                    }
                )
                ]),
                dbc.Row([
                    html.Div(
                    children='Correlation beetwen companies',
                    className="font-weight-bold text-center display-6 p-3 pt-5",
                    style={
                        'color': self.colors['text'],
                        'background-color': self.colors['bg']
                    }
                        )
                ]),
                dbc.Row([
                    dbc.Col(
                    dcc.Dropdown(
                        self.df_tickers["Symbol"] + " - " + self.df_tickers["FullName"],
                        id='correlation_dropdown',
                        className='pt-5 w-50 mx-auto',
                        style={'background-color': self.colors['bg'],'color': self.colors["text2"]}
                    )
                    ),
                    dbc.Col(
                    dcc.Dropdown(
                        self.df_tickers["Symbol"] + " - " + self.df_tickers["FullName"],
                        id='correlation2_dropdown',
                        className='pt-5 w-50 mx-auto',
                        style={'background-color': self.colors['bg'],'color': self.colors["text2"]}
                    )
                    )
                ],
                style={"margin-bottom": "20px"}
            ),
            dbc.Row([
                    dcc.Graph( id='corr_graph',figure={"layout":{
                        "template":"plotly_dark"
                    }})
                ]
                ),
                dbc.Row(
                    dbc.Col(
                        html.P(
                            f"\u00A9 All rights reserved. Made by Kacper Potaczała and Łukasz Cal.",
                            className="text-end text-white pt-3",
                        ),
                        width={"size": 12},
                        # style={"background-color": "#2E3135"}
                        style={'background-image': 'linear-gradient(#111111, #152559)'}
                    )
                )


        ],fluid=True,style={'background-color': self.colors['bg'],'overflow': 'auto','height':'100vh'})
        return content_layout