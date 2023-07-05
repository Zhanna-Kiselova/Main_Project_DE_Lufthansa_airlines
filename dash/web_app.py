import dash
from dash import dcc, Dash, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px 
import base64
import plotly.express as px

def generate_table(df):
    datatable = html.Div([
    dash_table.DataTable(
    id='datatable-interactivity',
    columns=[
    {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
    ],
    data=df.to_dict('records'),
    page_current=0,
    page_size=6,
    style_table={
    'overflowX': 'auto',
    'overflowY': 'auto',
    'maxHeight': '500px', 
    'maxWidth': '100%', 
    },
    style_data={
    'whiteSpace': 'normal',
    'height': 'auto',
    },
    style_cell={
    'textAlign': 'left',
    'minWidth': '120px', 
    'maxWidth': '180px', 
    'whiteSpace': 'no-wrap',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
    },
    style_header={
    'backgroundColor': 'rgb(230, 230, 230)',
    'fontWeight': 'bold',
    }
    ),
    ])

    return datatable


# lufthansa dataset
df1 = pd.read_csv('/home/ubuntu/Main_Project_DE_Lufthansa_airlines/fichiers_csv/flights_lufthansa_6833.csv', delimiter=',') # si web_app.py dans un le dossier principal : ('./fichiers_csv/flights_lufthansa_6833.csv', delimiter=',')

# airlabs dataset
df2 = pd.read_csv('/home/ubuntu/Main_Project_DE_Lufthansa_airlines/fichiers_csv/flights_airlabs_11068.csv', delimiter=',')
# lufthansa_airlines = ['LX', 'LH', 'EN', 'OS', 'WK', 'SN', '4Y']
# df2 = df2[df2['Airline_iata'].isin(lufthansa_airlines)]

# airport dataset 
df_airports = pd.read_csv('/home/ubuntu/Main_Project_DE_Lufthansa_airlines/fichiers_csv/airports_lufthansa_11108.csv', delimiter=',')


# Merging the dataframes based on the specified columns
merged_df = pd.merge(df1, df2, left_on='Compagnie', right_on='Airline_iata', how='inner')
# Removing duplicates from the merged dataframe
merged_df = merged_df.drop_duplicates()

# Example: Group by a column and aggregate using a function (e.g., sum)
# merged_df = merged_df.groupby('Flight_iata').agg({'OtherColumn': 'sum'}).reset_index()

accidents_depuis_1948 = pd.read_csv("/home/ubuntu/Main_Project_DE_Lufthansa_airlines/fichiers_csv/accidents_kaggle.csv")
city_weather_visualcrossing = pd.read_csv('/home/ubuntu/Main_Project_DE_Lufthansa_airlines/fichiers_csv/city_weather_visualcrossing_447.csv')




 
# CSS proposition 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Instantiation 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)


index_page = html.Div([
    html.H1('Lufthansa group flights dashboard', style={'color' : 'mediumturquoise', 'textAlign': 'center'}),
    # html.Button(dcc.Link('Flight status', href='/flight-status')),
    # html.Br(),
    # html.Button(dcc.Link('Statistics', href='/aviation-stats')),
    html.Br(),
    html.Button(dcc.Link('Weather alerts and global aviation statistics', href='/weather-data'))
], style={'alignItems': 'center'})

layout_page1 = html.Div([
  html.Div(dcc.Dropdown(id = 'Dropdown',
                        options= [{'label': 'LH-Lufthansa', 'value': 'LH'},
                                  {'label': 'EN-Air Dolomiti', 'value': 'EN'},
                                  {'label': 'LX-Swiss', 'value': 'LX'},
                                  {'label': 'OS-Austrian', 'value': 'OS'},
                                  {'label': 'SN-Brussels Airlines', 'value': 'SN'},
                                  {'label': '4Y-Eurowings Discover', 'value': '4Y'},
                                  {'label': 'WK-Edelweiss', 'value': 'WK'}
                                  ],
                        #value= 'LH'
  )),
# Map insertion
  html.Div([
    dcc.Graph(
        id='airplane-map',
    ),
    
   html.Div(id="table"),
]),
])
# Layout content
app.layout = html.Div([
    index_page,
# Title 
# html.H5('Real-time Lufthansa Group flights check-up status', style={'textAlign': 'center', 'color': '#f1c232'}),
html.Div([
    # Have the path to the application 
    dcc.Location(id='url', refresh=False),
    # Content of the page to be modified 
    html.Div(id='page-content', children=[
          layout_page1,
    ])
])

], style = {'background' : '#0F576D'})




# html.Div(children='Flights Status'),
# dash_table.DataTable(data=filtered_df.to_dict('records'), page_size=200)



#page 1 
@app.callback(
  [
    Output('airplane-map', 'figure'),
    Output('table', 'children')
   ],
   [
     Input('Dropdown', 'value'),
   ]
)
def update_graph(dropdown_value):
    if dropdown_value is None:
        filtered_df = merged_df
    else:
        filtered_df = merged_df[merged_df['Compagnie'] == dropdown_value]
    fig = go.Figure()
        # for i, row in merged_df.iterrows():
    fig.add_trace(
            go.Scattermapbox(
            lat=filtered_df['Latitude'],
            lon=filtered_df['Longitude'],
            mode='markers',
            marker=dict(
                size=8,
                color='mediumturquoise',
                # symbol='circle-dot',
                # opacity=0.8
            ),
            text=['<b>Location</b><br>Airplane Information</b><br>Flight: XYZ123<br>'],
        )
        )
        # Update the map layout
    fig.update_layout(
            mapbox=dict(
                accesstoken='pk.eyJ1Ijoiemhhbm5hLTI3IiwiYSI6ImNsaXhwaXl6MDBhNDAzcW8xcGphbWpjZjcifQ.VFeWpKtMClATXytM5q_U5g',
                bearing=0,
                # center=dict(
                #     lat=latitude,
                #     lon=longitude
                # ),
                # zoom=5,
            )
            # width= 400,
            # height = 1000
            # showlegend=False
        )
        
    filtered_df["Heure départ (en min LT)"] = filtered_df["Heure départ (en min LT)"]/60
    filtered_df["Heure arrivée (en min LT)"] = filtered_df["Heure arrivée (en min LT)"]/60
    columns = ["Lieu de départ IATA", "Lieu d'arrivée IATA", "Heure départ (en min LT)", "Date départ LT", "Heure arrivée (en min LT)", "Date arrivée LT", "Flight_iata",
    "Aircraft_icao", "Status"]
    filtered_df = filtered_df[columns]
    return [fig, generate_table(filtered_df.head())]
    
# Page 2
wheather_map = px.density_mapbox(city_weather_visualcrossing, lat='Latitude', lon='Longitude', z='Alerte_risk', radius=10,
                        center=dict(lat=0, lon=180), zoom=0,
                        hover_data=['Alerte_risk', 'Ville', 'Température_actuelle', 'Description_detailed', 'Conditions_météo','Alertes_météo'],
                        mapbox_style="stamen-terrain")
wheather_map.update_layout(
    title=dict(
        text="Real-time Global Weather Alerts ",
        font=dict(size=24),
        x=0.5,
        xref="paper"
    )
)
accidents_depuis_1948 = accidents_depuis_1948[accidents_depuis_1948['Investigation.Type'] == "Accident"]
accidents_depuis_1948['year'] = pd.DatetimeIndex(accidents_depuis_1948['Event.Date']).year
grouped_accidents_df = accidents_depuis_1948.groupby(['year']).agg({'Investigation.Type': 'count', 'Total.Fatal.Injuries' : 'sum'}).reset_index()
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

airlines_filtered = accidents_depuis_1948[accidents_depuis_1948['Air.carrier'].isin(['Air France', 'Lufthansa', 'Air Canada', 'American Airlines', 'United Airlines', 'British Airways',  'Japan Airlines', 'Ethiopian Airlines', 'Saudi Arabian Airlines', 'Ryanair', 'China Eastern Airlines', 'Mexicana Airlines', 'Royal Air Maroc', 'Air India', 'Malaysia Airlines'])]
airlines_filtered_grouped = airlines_filtered.groupby('Air.carrier')['Air.carrier'].count().reset_index(name="air-carrier-count")

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
    dcc.Graph(
        id='wheather-map',
        figure=wheather_map
    ),
    dcc.Graph(
        figure=accidents_fig
    ),
    dcc.Graph(
        figure=pie_chart
    )
])

# # Page 1
# layout_1 = html.Div([
#     html.H1('Flight status', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

#     html.Div(dcc.Graph(id='flight-status')),

#     html.Div(dcc.Slider(id = 'aviation-stats-slider',
#                       min = df['year'].min(),
#                       max = df['year'].max(),
#                       marks={str(year): str(year) for year in df['year'].unique()},
#                       step = None)),
#     html.Button(dcc.Link('Go back', href='/'))
# ], style = {'background' : '#0F576D'})

# @app.callback(Output(component_id='flight-status-graph', component_property='figure'),
#             [Input(component_id='flight-status-slider', component_property='value')])
# def update_graph(filter_year):
#     df_2 = df[df["year"] == filter_year]
#     # Creating the plotly figure
#     fig = px.scatter(df_2, x="gdpPercap",
#                      y = "lifeExp",
#                      color="continent",
#                      size="pop")
#     return fig

# Page 2

# layout_2 = html.Div([
#     html.H1('Aviation Statistics', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

#     html.Div(dcc.Graph(id='aviation-stats-graph')),

#     html.Div(dcc.Slider(id = 'aviation-stats-slider',
#                       min = df['year'].min(),
#                       max = df['year'].max(),
#                       marks={str(year): str(year) for year in df['year'].unique()},
#                       step = None)),
#     html.Button(dcc.Link('Go back', href='/'))
# ], style = {'background' : '#0F576D'})

# @app.callback(Output(component_id='aviation-stats-graph', component_property='figure'),
#             [Input(component_id='aviation-stats-slider', component_property='value')])
# def update_graph(filter_year):
#     df_2 = df[df["year"] == filter_year]
#     # Creating the plotly figure
#     fig = px.scatter(df_2, x="gdpPercap",
#                      y = "lifeExp",
#                      color="continent",
#                      size="pop")
#     return fig


# Page 3

# layout_3 = html.Div([
#   html.H1('Weather data and alerts', style={'textAlign': 'center', 'color': 'mediumturquoise'}),
#   html.Div(dcc.Dropdown(id = 'weather-data-dropdown',
#                         options= [{'label': 'life expandency', 'value': 'lifeExp'},
#                                   {'label': 'population', 'value': 'pop'}],
#                         value= 'lifeExp'
#   )),
#   html.Div(dcc.Graph(id='weather-data-graph')),
#   html.Button(dcc.Link('Go back', href='/'))
# ], style = {'background' : '#0F576D'})

# @app.callback(Output(component_id='weather-data-graph', component_property='figure'),
#             [Input(component_id='weather-data-dropdown', component_property='value')])
# def update_graph_1(indicator):
#     # Creating the plotly figure
#     fig = px.scatter_geo(df_1, locations="iso_alpha", color=indicator,
#                      hover_name="country", size="pop",
#                      projection="natural earth")
#     return fig



# Index update
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    # elif pathname == '/aviation-stats':
    #     return layout_2
    if pathname == '/weather-data':
        return layout_page2
    else:
        raise dash.exceptions.PreventUpdate

# to launch with Flask  
if __name__ == '__main__':
  app.run_server(debug=True, host = '0.0.0.0')

