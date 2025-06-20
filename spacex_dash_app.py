# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
csv_path = os.path.join(os.path.dirname(__file__), "spacex_launch_dash.csv")
spacex_df = pd.read_csv(csv_path)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Clamp payload values to slider range
min_payload = max(0, min(min_payload, 10000))
max_payload = min(10000, max_payload)

# Create a dash application
app = dash.Dash(__name__)
server = app.server

uniquelaunchsites = spacex_df['Launch Site'].unique().tolist()
lsites = []
lsites.append({'label': 'All Sites', 'value': 'All Sites'})
for site in uniquelaunchsites:
    lsites.append({'label': site, 'value': site})

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site_dropdown', options=lsites, placeholder='Select a Launch Site here',
                 searchable=True, value='All Sites'),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart', style={'height': '500px'})),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload_slider',
        min=0,
        max=10000,
        step=1000,
        marks={
            0: '0 kg',
            1000: '1000 kg',
            2000: '2000 kg',
            3000: '3000 kg',
            4000: '4000 kg',
            5000: '5000 kg',
            6000: '6000 kg',
            7000: '7000 kg',
            8000: '8000 kg',
            9000: '9000 kg',
            10000: '10000 kg'
        },
        value=[min_payload, max_payload]
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart', style={'height': '500px'})),
])

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value')]
)
def update_graph(site_dropdown):
    if site_dropdown == 'All Sites':
        df = spacex_df[spacex_df['class'] == 1]
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="No successful launches for All Sites",
                               xref="paper", yref="paper", showarrow=False, font=dict(size=20))
            fig.update_layout(title="Total Success Launches By all sites", height=400)
            return fig
        fig = px.pie(df, names='Launch Site', hole=.3, title='Total Success Launches By all sites')
    else:
        df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text=f"No data for {site_dropdown}",
                               xref="paper", yref="paper", showarrow=False, font=dict(size=20))
            fig.update_layout(title=f"Total Success Launches for site {site_dropdown}", height=400)
            return fig
        fig = px.pie(df, names='class', hole=.3, title=f'Total Success Launches for site {site_dropdown}')
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
    return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value'),
     Input(component_id="payload_slider", component_property="value")]
)
def update_scattergraph(site_dropdown, payload_slider):
    low, high = payload_slider
    if site_dropdown == 'All Sites':
        df = spacex_df
    else:
        df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
    mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
    filtered_df = df[mask]
    if filtered_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data for selected filters",
                           xref="paper", yref="paper", showarrow=False, font=dict(size=20))
        fig.update_layout(title="Payload Mass vs Launch Outcome", xaxis_title="Payload Mass (kg)",
                          yaxis_title="Class", height=400)
        return fig
    fig = px.scatter(
        filtered_df, x="Payload Mass (kg)", y="class",
        color="Booster Version",
        size='Payload Mass (kg)',
        hover_data=['Payload Mass (kg)']
    )
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
    return fig
