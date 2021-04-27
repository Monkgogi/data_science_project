import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from pathlib import Path

app = dash.Dash(__name__)

# Preparing the data for the line graph
data_folder = Path('../data')
Excel_file = 'international-visitors-london.xlsx'
data = pd.read_excel(data_folder / Excel_file, sheet_name='By duration', skiprows=1)
data.loc[18, 'Year/Nights'] = 2020

fig_line = go.Figure()

fig_line.add_trace(go.Scatter(x=data['Year/Nights'], y=data['Total.3'], name='Sample size'))
fig_line.add_trace(go.Scatter(x=data['Year/Nights'], y=data['Total.2'], name='Total spend (£m)'))
fig_line.add_trace(go.Scatter(x=data['Year/Nights'], y=data['Total.1'], name='Total nights'))

labels = ['Sample size', 'Total spend (£m)', 'Total nights']

fig_line.add_annotation(x=2006, y=101067, text='Change of Total nights', showarrow=False, yshift=12)
fig_line.add_annotation(x=2006, y=24206, text='Change of Sample size', showarrow=False, yshift=12)
fig_line.add_annotation(x=2006, y=7821, text='Change of Total spend (£m)', showarrow=False, yshift=12)

fig_line.update_layout(title='Change of the total nights, spend(£m) and the sample size from 2002 until 2020',
                       xaxis_title='Years',
                       xaxis=dict(showgrid=False), showlegend=False)


# Preparing the data for the bar charts
list_options = ['Total Visits', 'Total Nights', 'Total Spend (£m)', 'Sample size']
Data = pd.read_excel(data_folder / Excel_file, sheet_name='By quarter')
Data.loc[72, 'Year'] = 2020
Data.rename(columns={'Total Visits (000s)': 'Total Visits', 'Total Nights (000s)': 'Total Nights'}, inplace=True)


# Create a Dash app

def init_dashboard(flask_app):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=flask_app,
                         routes_pathname_prefix="/dash_app/",
                         external_stylesheets=[dbc.themes.LITERA],
                         )

    dash_app.layout = dbc.Container(fluid=True, children=[
        html.Br(),
        html.H1("DATA VISUALISATIONS FOR COURSEWORK 1",
                style={'text-align': 'center'}),
        dbc.Row([
            dbc.Col(width=3, children=[
                dbc.FormGroup([
                    html.H4("Select value for the bar chart"),
                    dcc.Dropdown(id='Total',
                                 options=[{'label': i, 'value': i} for i in list_options],
                                 value='Total Visits'),

                ]),
                html.Br(),
                html.Div(id="output-panel"),
            ]),
            dbc.Col([
                    dcc.Graph(id="Bar chart")
            ]),
        ]),
        html.Br(),
        dbc.Row([
            dcc.Graph(id="Line graph", figure=fig_line)
        ])
    ])

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(Output('Bar chart', 'figure'),[Input('Total', 'value')])
    def update_graph(value):
        fig = px.bar(Data, x='Year', y=value, color='Quarter', hover_name='Quarter')
        fig.update_layout(title='Change of "{}" for each quarter per year'.format(value))

        return fig
