# app.py

import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load SpaceX data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Launch sites list
launch_sites = [{'label': 'All Sites', 'value': 'All Sites'}] + \
               [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Dash app
app = dash.Dash(__name__)
server = app.server

# Layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 40}),

    dcc.Dropdown(
        id='site_dropdown',
        options=launch_sites,
        value='All Sites',
        placeholder='Select a Launch Site',
        searchable=True
    ),
    html.Br(),

    dcc.Graph(id='success-pie-chart'),
    html.Br(),

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload_slider',
        min=0, max=10000, step=1000,
        value=[min_payload, max_payload],
        marks={i: f'{i} kg' for i in range(0, 10001, 1000)}
    ),
    html.Br(),

    dcc.Graph(id='success-payload-scatter-chart')
])

# Pie chart callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site_dropdown', 'value')
)
def update_pie(selected_site):
    if selected_site == 'All Sites':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
            filtered_df,
            names='Launch Site',
            title='Total Successful Launches by Site',
            hole=0.3
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        counts = filtered_df['class'].value_counts().reset_index()
        counts.columns = ['class', 'count']
        counts['class'] = counts['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            counts,
            names='class',
            values='count',
            title=f'Success vs Failure for {selected_site}',
            hole=0.3
        )
    return fig

# Scatter plot callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site_dropdown', 'value'),
     Input('payload_slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    if selected_site != 'All Sites':
        df = df[df['Launch Site'] == selected_site]

    fig = px.scatter(
        df, x='Payload Mass (kg)', y='class',
        color='Booster Version',
        size='Payload Mass (kg)',
        hover_data=['Payload Mass (kg)'],
        title='Payload vs Success Correlation'
    )
    return fig
