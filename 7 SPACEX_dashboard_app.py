# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

opts = [
    {'label': name, 'value': name}
    for name in sorted(spacex_df['Launch Site'].unique())
]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'}] + opts,
                                    placeholder='Select a Launch Site here',
                                    searchable=True,
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload],
                                    marks={
                                        0: '0', 
                                        2000: '2000',
                                        4000: '4000',
                                        6000: '6000',
                                        8000: '8000', 
                                        10000: '10000',
                                    }
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        pie_chart = px.pie(
            spacex_df, # all data
            names='Launch Site',
            values='class',
            title='Total Launches for All Sites',
        )
        return pie_chart
    else:
        # selected site only
        filtered_data = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        pie_chart = px.pie(
            filtered_data, 
            names='class',
            title=f'Total Launches for {entered_site}',
        )
        return pie_chart


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value'),
    ]
)

def update_scatter_chart(entered_site, entered_payload):
    if entered_site == 'ALL':
        # filter only by Pyload, we need all Sites here
        data = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= entered_payload[0]) &
            (spacex_df['Payload Mass (kg)'] <= entered_payload[1])
        ]
        title = 'Correlation between Payload and Success for All Sites'

    else:
        # first, filter by selected Site
        site_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        # then filter by Payload
        data = site_df[
            (site_df['Payload Mass (kg)'] >= entered_payload[0]) &
            (site_df['Payload Mass (kg)'] <= entered_payload[1])
        ]
        title = f'Correlation between Payload and Success for {entered_site}'

    # render scatter chart
    scatter_chart = px.scatter(
        data,
        title=title,
        x='Payload Mass (kg)',
        y='class', 
        color='Booster Version Category'
    )
    return scatter_chart


# Run the app
if __name__ == '__main__':
    app.run_server()
