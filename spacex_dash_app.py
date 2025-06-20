# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import os

# Read the data into pandas dataframe
csv_path = os.path.join(os.path.dirname(__file__), "spacex_launch_dash.csv")
try:
    spacex_df = pd.read_csv(csv_path)
except FileNotFoundError:
    print("Error: spacex_launch_dash.csv not found. Ensure the file is in the same directory.")
    raise

# Validate required columns
required_columns = ['Launch Site', 'class', 'Payload Mass (kg)', 'Booster Version']
if not all(col in spacex_df.columns for col in required_columns):
    print(f"Error: CSV missing required columns. Found: {spacex_df.columns.tolist()}")
    raise ValueError("Missing required columns in CSV")

# Calculate payload range for slider
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
min_payload = max(0, min(min_payload, 10000))  # Clamp to slider range
max_payload = min(10000, max_payload)

# Create a dash application
app = dash.Dash(__name__)
server = app.server

# Create dropdown options for launch sites
uniquelaunchsites = spacex_df['Launch Site'].unique().tolist()
lsites = [{'label': 'All Sites', 'value': 'All Sites'}] + [
    {'label': site, 'value': site} for site in uniquelaunchsites
]

# Create app layout
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
        marks={i: f'{i} kg' for i in range(0, 11000, 1000)},
        value=[min_payload, max_payload]
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart', style={'height': '500px'})),
])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site_dropdown', 'value')]
)
def update_graph(site_dropdown):
    if site_dropdown == 'All Sites':
        df = spacex_df[spacex_df['class'] == 1]
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="No successful launches for All Sites",
                               xref="paper", yref="paper", showarrow=False, font=dict(size=20))
            fig.update_layout(title="Total Success Launches By All Sites", height=400)
            return fig
        fig = px.pie(df, names='Launch Site', hole=.3, title='Total Success Launches By All Sites')
    else:
        df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text=f"No data for {site_dropdown}",
                               xref="paper", yref="paper", showarrow=False, font=dict(size=20))
            fig.update_layout(title=f"Total Success Launches for {site_dropdown}", height=400)
            return fig
        fig = px.pie(df, names='class', hole=.3, title=f'Total Success Launches for {site_dropdown}')
        fig.update_traces(textinfo='percent+label', pull=[0.1, 0])  # Improve readability
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# Callback for scatter plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site_dropdown', 'value'), Input('payload_slider', 'value')]
)
def update_scattergraph(site_dropdown, payload_slider):
    low, high = payload_slider
    df = spacex_df if site_dropdown == 'All Sites' else spacex_df[spacex_df['Launch Site'] == site_dropdown]
    mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] <= high)  # Include upper bound
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
        hover_data=['Payload Mass (kg)'],
        title="Payload Mass vs Launch Outcome"
    )
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
    fig.update_yaxes(tickvals=[0, 1], ticktext=['Failure (0)', 'Success (1)'])  # Clarify y-axis
    return fig

