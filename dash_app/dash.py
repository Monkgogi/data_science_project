from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# The data

data_folder = Path('../data')
Excel_file = 'dataset_3.xlsx'
df2 = pd.read_excel(data_folder / Excel_file)


# fb = pd.read_csv("dataset_1.csv")
# df = pd.read_excel('international-visitors-london (1).xlsx', sheet_name='By duration')

# Create a Dash app
def init_dashboard(flask_app):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=flask_app,
                         routes_pathname_prefix="/dash_app/",
                         )
    dash_app.layout = html.Div(children=[

        html.Div([
            html.Label(['X-axis categories to compare:'], style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='xaxis_raditem',
                options=[{'label': 'Years', 'value': 'Year'}],
                value='Year',
                style={"width": "50%"}
            ),
        ]),

        html.Div([
            html.Br(),
            html.Label(['Y-axis values to compare:'], style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='yaxis_raditem',
                options=[
                    {'label': 'Total sample', 'value': 'Total sample'},
                    {'label': 'Total spent', 'value': 'Total spent'}, ],
                value='Total sample',
                style={"width": "50%"}
            ),
        ]),

        html.Div([
            dcc.Graph(id='the_graph')
        ]),
    ])
    init_callbacks(dash_app)
    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(
            Output(component_id='the_graph', component_property='figure'),
            [Input(component_id='xaxis_raditem', component_property='value'),
             Input(component_id='yaxis_raditem', component_property='value')]
    )
    def update_graph(x_axis, y_axis):
        dff = df2

        barchart = px.bar(
                data_frame=dff,
                x=x_axis,
                y=y_axis,

                title=x_axis + ': by ' + y_axis,

        )

        barchart.update_layout(xaxis={'categoryorder': 'total ascending'},
                                   title={'xanchor': 'center', 'yanchor': 'top', 'y': 0.9, 'x': 0.5, })

    return dash_app.server
