import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import Dash
from dash.dependencies import Input, Output
from pathlib import Path

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

fig = px.bar(Data, x='Year', y='Total Visits', color='Quarter', hover_name='Quarter')
fig.update_layout(title='Change of "{}" for each quarter per year'.format('Total Visits'))

fig2 = px.bar(Data, x='Year', y='Total Nights', color='Quarter', hover_name='Quarter')
fig2.update_layout(title='Change of "{}" for each quarter per year'.format('Total Visits'))

fig3 = px.bar(Data, x='Year', y='Total Spend (£m)', color='Quarter', hover_name='Quarter')
fig3.update_layout(title='Change of "{}" for each quarter per year'.format('Total Spend (£m)'))

fig4 = px.bar(Data, x='Year', y='Sample size', color='Quarter', hover_name='Quarter')
fig4.update_layout(title='Change of "{}" for each quarter per year'.format('Sample size'))


# Create a Dash app
class DashApp1:
    def __init__(self, flask_server):
        self.app = Dash(name=self.__class__.__name__,
                        routes_pathname_prefix='/dash_app1/',
                        suppress_callback_exceptions=True,
                        server=flask_server,
                        external_stylesheets=[dbc.themes.LUX],
                        meta_tags=[{
                            'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'
                        }]
                        )

    def setup(self):
        self.setup_layout()

    def setup_layout(self):
        self.app.layout = dbc.Container(fluid=True, children=[
            html.Br(),
            html.H1("DATA VISUALISATIONS FOR COURSEWORK 1",
                    style={'text-align': 'center'}),
            html.Br(),
            dbc.Row([

                dbc.Col([
                    dbc.Tabs(className="nav nav-pills", children=[
                        dbc.Tab(dcc.Graph(id="Bar chart 1", figure=fig), label='Total Visits'),
                        dbc.Tab(dcc.Graph(id="Bar chart 2", figure=fig2), label='Total Nights'),
                        dbc.Tab(dcc.Graph(id="Bar chart 3", figure=fig3), label='Total Spend (£m)'),
                        dbc.Tab(dcc.Graph(id="Bar chart 4", figure=fig4), label='Sample size')
                    ])
                ]),
            ]),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="Line graph", figure=fig_line)
                ])
            ])
        ])
