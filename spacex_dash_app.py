# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)
server = app.server  # For deployment

# Dropdown options
launch_sites = spacex_df['Launch Site'].unique().tolist()
site_options = [{'label': 'All Sites', 'value': 'All Sites'}] + \
               [{'label': site, 'value': site} for site in launch_sites]

# App layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 40}),

    dcc.Dropdown(
        id='site_dropdown',
        options=site_options,
        value='All Sites',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    html.Br(),

    dcc.Graph(id='success-pie-chart'),
    html.Br(),

    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload_slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i} kg' for i in range(0, 10001, 1000)},
        value=[min_payload, max_payload]
    ),

    html.Br(),
    dcc.Graph(id='success-payload-scatter-chart')
])

# Pie Chart Callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site_dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'All Sites':
        df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
            df,
            names='Launch Site',
            title='Total Successful Launches by Site',
            hole=0.3
        )
    else:
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
        outcome_counts = df['class'].value_counts().reset_index()
        outcome_counts.columns = ['class', 'count']
        outcome_counts['class'] = outcome_counts['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            outcome_counts,
            names='class',
            values='count',
            title=f'Success vs. Failure for {selected_site}',
            hole=0.3
        )
    return fig

# Scatter Plot Callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site_dropdown', 'value'),
     Input('payload_slider', 'value')]
)
def update_scatter_plot(selected_site, payload_range):
    low, high = payload_range
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                   (spacex_df['Payload Mass (kg)'] <= high)]

    if selected_site != 'All Sites':
        df = df[df['Launch Site'] == selected_site]

    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version',
        size='Payload Mass (kg)',
        hover_data=['Payload Mass (kg)'],
        title='Payload vs. Launch Outcome by Booster Version'
    )
    return fig


