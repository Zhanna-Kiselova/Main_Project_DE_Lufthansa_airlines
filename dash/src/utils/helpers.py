from dash import html, dash_table  
import os # to find the files easier in the subfolders type 
import pandas as pd # for dataframe 
from requests import get, put # for getting info from the websites via API 
import json # for transferring into a dictionnary .json (accepted for mongodb)
from datetime import datetime 

# local import
from .settings import API_KEY_WEATHER, AIRLABS_API_KEY

FAST_API_URL = os.environ.get('FAST_API_URL')

cwd = os.getcwd() # varibale for defining the current working directory 

# Function to generate a table in Dash, defining the structure (1st page)
def generate_table(df):
    datatable = html.Div([  # defining name section "datatable" for the table in Dash
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
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


# Function to get the flights from mongodb using fastapi endopint
def get_flight_airlabs_mongo_db():
    flight_airlabs = get(f"{FAST_API_URL}get_flights_data")
    flight_airlabs = flight_airlabs.json()
    flight_airlabs = json.loads(flight_airlabs)
    flight_airlabs = pd.DataFrame(flight_airlabs)
    return flight_airlabs

# Function to get the airports from mongodb using fastapi endopint
def get_airports_mongo_db():
    airports = get(f"{FAST_API_URL}get_airports_data")
    airports = airports.json()
    airports = json.loads(airports)
    airports = pd.DataFrame(airports)
    return airports

# Function to get the weather from mongodb using fastapi endpoint
def get_df_weather_mongo_db():
    df_weather = get(f"{FAST_API_URL}get_weather_data")
    df_weather = df_weather.json()
    df_weather = json.loads(df_weather)
    df_weather = pd.DataFrame(df_weather)
    return df_weather

# Function to get the accidents from mongodb using fastapi endpoint
def get_accidents_mongo_db():
    df_accidents = get(f"{FAST_API_URL}get_accidents_data")
    df_accidents = df_accidents.json()
    df_accidents = json.loads(df_accidents)
    df_accidents = pd.DataFrame(df_accidents)
    return df_accidents

# Function to get the airports from mongodb using fastapi endopint
def get_airports_mongo_db():
    airports = get(f"{FAST_API_URL}get_airports_data")
    airports = airports.json()
    airports = json.loads(airports)
    airports = pd.DataFrame(airports)
    return airports

# Here below the functions to get the real-time data from API of visualcrossing website 
def get_city_weather_api(): 
    try:
        airports_ourairports= get_airports_mongo_db() # Using "airports_ourairports" collection from mongodb to get cities 
        cities = airports_ourairports['municipality'].unique() # We need to precise a list of cities in the api endpoint of visualcrossing in order to get the weather
        df_weather= pd.DataFrame(columns = ['City', 'Description jour', 'Timezone', 'Latitude', 'Longitude', 'Date', 'Current time', 'Max_Température', 'Min_Température', 'Current temperature',
                                                'Humidité','Precipitation', 'Neige', 'Neige_densité', 'Vent_rafale', 'Vent_vitesse','Vent_direction', 'Pression', 'Nuage', 'Visibilité',
                                                'Solar radiation','Energy_solaire', 'Soleil_coucher', 'Alert risk','Description', 'Weather conditions', 'Weather alerts',
                                                'Alertes_description','Vitesse_vent'])
        c = 0
        for city_name in cities:
            if city_name == None: 
                continue
            url= f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}?unitGroup=metric&key={API_KEY_WEATHER}&contentType=json"
            resp2 = get(url)
            if resp2.status_code != 200:
                continue
            visual = resp2.json()
            c += 1
            if c%10 == 0: 
                print(c)
            # try:
            #print(visual)
            row = pd.DataFrame({'City': [visual['resolvedAddress']],
                                'Description jour': visual['description'],
                                'Timezone': visual['timezone'],
                                'Latitude': visual['latitude'],
                                'Longitude': visual['longitude'],
                                'Date': visual['days'][0]['datetime'],
                                'Current time': visual['currentConditions']['datetime'],
                                'Max_Température': visual['days'][0]['tempmax'],
                                'Min_Température': visual['days'][0]['tempmin'],
                                'Current temperature': visual['currentConditions']['temp'],
                                'Humidité': visual['days'][0]['humidity'],
                                'Precipitation': visual['days'][0]['precip'],
                                'Neige': visual['days'][0]['snow'],
                                'Neige_densité': visual['days'][0]['snowdepth'],
                                'Vent_rafale': visual['days'][0]['windgust'],
                                'Vent_vitesse': visual['days'][0]['windspeed'],
                                'Vent_direction': visual['days'][0]['winddir'],
                                'Pression': visual['days'][0]['pressure'],
                                'Nuage': visual['days'][0]['cloudcover'],
                                'Solar radiation': visual['days'][0]['solarradiation'],
                                'Energy_solaire': visual['days'][0]['solarenergy'],
                                'Soleil_coucher': visual['days'][0]['sunset'],
                                'Alert risk': visual['days'][0]['severerisk'],
                                'Description': visual['days'][0]['description'],
                                'Weather conditions': visual['days'][0]['conditions'],
                                'Weather alertes': visual['alerts'][0]['event'] if visual["alerts"] else None,
                                'Alertes_description': visual['alerts'][0]['description'] if visual["alerts"] else None,
                                'Vitesse_vent': visual['days'][0]['windspeed']})
            df_weather = pd.concat([df_weather, row], ignore_index=True)
        #print(df_weather)
            #return df_weather
            if not df_weather.empty:
                df_weather_json = df_weather.to_json(orient="records") # Converting filetered dataframe to .json
                payload = {'data' : df_weather_json} # data variable used in fastapi endpoint function def insert_weather()
                response = put(f"{FAST_API_URL}insert_weather_data", json=payload) # inserting real-time data into mongodb by crushing the old one, using fastapi endpoint
                print(response)
            else:
                df_weather = get_df_weather_mongo_db() # If API visualcrossing restricted or bug, getting latest weather from mongodb (function on top of the page)
    except:
        df_weather = get_df_weather_mongo_db() # If API visualcrossing restricted or bug, getting latest weather from mongodb (function on top of the page)
    return df_weather


# API request function for the airlabs site to get the real-time flights status 
def get_flight_airlabs_api():
    # return flight_airlabs
    try:
        flight_airlabs = get(f"https://airlabs.co/api/v9/flights?api_key={AIRLABS_API_KEY}")
        flight_airlabs = flight_airlabs.json()
        flight_airlabs = pd.DataFrame([[flight.get('reg_number'),
                            flight.get("flag"),
                            flight.get("lat"),
                            flight.get("lng"),
                            flight.get("alt"),
                            flight.get("dir"),
                            flight.get("speed"),
                            flight.get("flight_number"),
                            flight.get("flight_icao"),
                            flight.get("flight_iata"),
                            flight.get("dep_icao"),
                            flight.get("dep_iata"),
                            flight.get("arr_icao"),
                            flight.get("arr_iata"),
                            flight.get("airline_icao"),
                            flight.get("airline_iata"),
                            flight.get("aircraft_icao"),
                            flight.get("updated"),
                            flight.get("status")] for flight in flight_airlabs["response"]],
                            columns=['Registration_number', 'Flag', 'Latitude', 'Longitude', 'Altitude', 'Direction', 'Speed', 'Flight_number', 'Flight_icao', 'Flight_iata',
                                    'Departure_icao', 'Departure_iata', 'Arrival_icao', 'Arrival_iata', 'Airline_icao', 'Airline_iata', 'Aircraft_icao', 'Updated', 'Status',])
        flight_airlabs['Updated'] = flight_airlabs['Updated'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')) # https://www.epochconverter.com/ to convert timestamp into human date
        flight_airlabs_json = flight_airlabs.to_json(orient="records") # Converting filetered dataframe to .json
        payload = {'data' : flight_airlabs_json} # data variable used in fastapi endpoint function def insert_airlabs()
        response = put(f"{FAST_API_URL}insert_airlabs_data", json=payload) # inserting real-time data into mongodb by crushing the old one, using fastapi endpoint
        print(response)
    except:
        flight_airlabs = get_flight_airlabs_mongo_db() # If API airlabs restricted or bug, getting latest flights from mongodb (function on top of the page)
        flight_airlabs['Updated'] = flight_airlabs['Updated'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')) # https://www.epochconverter.com/ to convert timestamp into human date

    return flight_airlabs
