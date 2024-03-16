import plotly_express as px
class ChangeGraphs:
    def __init__(self, df):
        self.df = df
    def changeGraphToBox(self, col_chosen):
        figure= px.box(self.df,x='city',y=col_chosen,color='city',template= 'plotly_dark',title='place for chart title')
        figure.update_layout(
            font_family='Courier New',
            font_size=13,
            title_font_family="Times New Roman",
            title_font_size=20
        )
        return figure
    def changeGraphToHistogram(self, col_chosen):
        figure= px.histogram(self.df,x=col_chosen,color='city',template= 'plotly_dark',title='place for chart title')
        figure.update_layout(
            font_family='Courier New',
            font_size=13,
            title_font_family="Times New Roman",
            title_font_size=20
        )
        return figure