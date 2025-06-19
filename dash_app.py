import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the CSV file
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get the min and max payload
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Dropdown options
launch_sites = spacex_df['Launch Site'].unique().tolist()
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# App layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    dcc.Dropdown(id='site_dropdown',
                 options=dropdown_options,
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True),
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    dcc.RangeSlider(id='payload_slider',
                    min=0, max=10000, step=500,
                    marks={i: f'{i}kg' for i in range(0, 10001, 1000)},
                    value=[min_payload, max_payload]),

    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Pie chart callback
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site_dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df, names='Launch Site', title='Total Successful Launches by Site')
    else:
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(df, names='class',
                     title=f'Total Success vs Failure for site {selected_site}',
                     hole=0.3)
    return fig

# Scatter plot callback
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value'),
     Input(component_id="payload_slider", component_property="value")]
)
def update_scatter_plot(selected_site, payload_range):
    low, high = payload_range
    df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site != 'ALL':
        df_filtered = df_filtered[df_filtered['Launch Site'] == selected_site]
    
    fig = px.scatter(df_filtered,
                     x="Payload Mass (kg)",
                     y="class",
                     color="Booster Version",
                     hover_data=["Launch Site", "Booster Version"],
                     title=f'Payload vs Success for {"all sites" if selected_site == "ALL" else selected_site}')
    return fig
