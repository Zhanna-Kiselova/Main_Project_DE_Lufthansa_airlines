from dash import dcc, html, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd

# local imports
from ..utils.helpers import get_flight_airlabs_api, generate_table
from ..utils.settings import API_KEY_MAPBOX

# Definition of a variable for the page 1 layout
layout_page1 = html.Div([
    html.Div(dcc.Dropdown(id='Dropdown',
                        options=[{'label': 'LH-Lufthansa', 'value': 'LH'},
                                 {'label': 'EN-Air Dolomiti', 'value': 'EN'},
                                 {'label': 'LX-Swiss', 'value': 'LX'},
                                 {'label': 'OS-Austrian', 'value': 'OS'},
                                 {'label': 'SN-Brussels Airlines', 'value': 'SN'},
                                 {'label': '4Y-Eurowings Discover', 'value': '4Y'},
                                 {'label': 'WK-Edelweiss', 'value': 'WK'}
                                 ],
                        # value= 'LH'
                          )),
    # Map insertion
    html.Div([
        dcc.Graph(
            id='airplane-map',
        ),
        # Table insertion
        html.Div(id="table"),
    ]),
])




# Page 1
@callback(
    [
        Output('airplane-map', 'figure'),
        Output('table', 'children')
    ],
    [
        Input('Dropdown', 'value'),
    ]
)
def update_graph(dropdown_value):
    flight_airlabs = get_flight_airlabs_api()
    if dropdown_value is None:
        filtered_df = flight_airlabs
    else:
        filtered_df = flight_airlabs[flight_airlabs['Airline_iata']
                                     == dropdown_value]
    fig = go.Figure()
    filtered_df['combined']= list(zip(filtered_df['Status'], filtered_df['Updated']))
    hovertemplate = """
    <b>%{text}</b><br>
    Latitude: %{lat:.2f}<br>
    Longitude: %{lon:.2f}<br>
    Status: %{customdata[0]}<br>
    Updated: %{customdata[1]} 
    <extra></extra>
    """
    fig.add_trace(
        go.Scattermapbox(
            lat=filtered_df['Latitude'],
            lon=filtered_df['Longitude'],
            mode='markers',
            marker=dict(
                size=8,
                color='mediumturquoise',

            ),
            text=filtered_df['Flight_iata'],
            customdata=filtered_df['combined'],
            hovertemplate=hovertemplate
        )
    )
    # Update the map layout
    fig.update_layout(
        mapbox=dict(
            accesstoken=API_KEY_MAPBOX,
            bearing=0,
        )
    )

    columns = ["Departure_iata", "Arrival_iata", "Flight_iata", "Airline_iata", "Flag",
               "Aircraft_icao", "Updated", "Status"]
    filtered_df = filtered_df[columns]
    return [fig, generate_table(filtered_df)]