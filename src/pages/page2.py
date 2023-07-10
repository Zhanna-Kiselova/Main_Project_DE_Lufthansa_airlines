from dash import dcc, html, callback, Input, Output
import dash
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
# local imports
from ..utils.helpers import get_accidents_csv, get_city_weather_csv, get_city_weather_api


city_weather_visualcrossing = get_city_weather_csv()
accidents_depuis_1948 = get_accidents_csv()

# Page 2
# website to adapt the color for the coloscale of a bar in the heat map : https://plotly.com/python/colorscales/
wheather_map = px.density_mapbox(city_weather_visualcrossing, lat='Latitude', lon='Longitude', z='Alert risk', radius=10,
                                 center=dict(lat=0, lon=180), zoom=0,
                                 hover_data=['Alert risk', 'City', 'Current temperature', 'Date', 'Current time',
                                             'Description', 'Solar radiation', 'Weather conditions', 'Weather alerts'],
                                 mapbox_style="carto-positron",
                                 color_continuous_scale="mint"  # gnbu # greys #gray # deep #teal # pubugn # mint
                                 )
wheather_map.update_layout(
    title=dict(
        text="Real-time Global Weather Alerts",
        font=dict(size=24),
        x=0.5,
        xref="paper"
    )
)
accidents_depuis_1948 = accidents_depuis_1948[accidents_depuis_1948['Investigation.Type'] == "Accident"]
accidents_depuis_1948['year'] = pd.DatetimeIndex(
    accidents_depuis_1948['Event.Date']).year
grouped_accidents_df = accidents_depuis_1948.groupby(['year']).agg(
    {'Investigation.Type': 'count', 'Total.Fatal.Injuries': 'sum'}).reset_index()
accidents_fig = go.Figure()
accidents_fig.add_trace(go.Scatter(
    x=grouped_accidents_df['year'],
    y=grouped_accidents_df['Investigation.Type'],
    mode='lines',
    name='Accidents'
))
accidents_fig.add_trace(go.Scatter(
    x=grouped_accidents_df['year'],
    y=grouped_accidents_df['Total.Fatal.Injuries'],
    mode='lines',
    name='Injuries'
))
accidents_fig.update_layout(
    title=dict(
        text="Evolution of # of all types of air crashes VS # of fatal injuries 1948-2022 (source : Kaggle)",
        font=dict(size=24),
        x=0.5,
        xref="paper"
    )
)

airlines_filtered = accidents_depuis_1948[accidents_depuis_1948['Air.carrier'].isin(['Air France', 'Lufthansa', 'Air Canada', 'American Airlines', 'United Airlines', 'British Airways',
                                                                                    'Japan Airlines', 'Ethiopian Airlines', 'Saudi Arabian Airlines', 'Ryanair', 'China Eastern Airlines', 'Mexicana Airlines', 'Royal Air Maroc', 'Air India', 'Malaysia Airlines'])]
airlines_filtered_grouped = airlines_filtered.groupby(
    'Air.carrier')['Air.carrier'].count().reset_index(name="air-carrier-count")

pie_chart = go.Figure([
    go.Pie(labels=airlines_filtered_grouped['Air.carrier'], values=airlines_filtered_grouped['air-carrier-count'],
           textinfo='label',
           insidetextorientation='radial')

])
pie_chart.update_layout(
    title=dict(
        text="Air crashes by air carrier 1948-2022 (source : Kaggle)",
        font=dict(size=24),
        x=0.5,
        xref="paper"
    )
)


layout_page2 = html.Div([
    html.Button("Update Map", id="wheather-update-btn", n_clicks=0),
    dcc.Graph(
            id='wheather-map',  # id to be called in callback in Input and Output
            figure=wheather_map  # property to be called in callback in Input and Output
        ),
    dcc.Loading(
        id="loading",
        type="default",
    ),
    dcc.Graph(
        figure=accidents_fig
    ),
    dcc.Graph(
        figure=pie_chart
    )
])


@callback(
    [Output('wheather-map', 'figure'),
     Output('loading', 'children')],
    Input('wheather-update-btn', 'n_clicks')
)
def update_wheather_data(n_clicks):
    if n_clicks > 0:
        city_weather_visualcrossing = get_city_weather_api()
        wheather_map = px.density_mapbox(city_weather_visualcrossing, lat='Latitude', lon='Longitude', z='Alert risk', radius=10,
                                         center=dict(lat=0, lon=180), zoom=0,
                                         hover_data=['Alert risk', 'City', 'Current temperature', 'Date', 'Current time',
                                             'Description', 'Solar radiation', 'Weather conditions', 'Weather alerts'],
                                         mapbox_style="carto-positron",
                                         color_continuous_scale="mint"  # gnbu # greys #gray # deep #teal # pubugn # mint
                                         )
        wheather_map.update_layout(
            title=dict(
                text="Real-time Global Weather Alerts",
                font=dict(size=24),
                x=0.5,
                xref="paper"
            )
        )

        return [wheather_map, html.Div(None)]
    else:
        raise dash.exceptions.PreventUpdate
