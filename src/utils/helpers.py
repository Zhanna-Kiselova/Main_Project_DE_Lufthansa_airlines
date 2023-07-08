from dash import html, dash_table
import os
import pandas as pd
from requests import get

# local import

from .settings import API_KEY_WEATHER
from .mongo_database import get_airlabs_data, insert_airlabs_data

cwd = os.getcwd()


def generate_table(df):
    datatable = html.Div([
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


def get_accidents_csv():
    file_path = os.path.join(cwd, 'fichiers_csv', "accidents_kaggle.csv")
    accidents_depuis_1948 = pd.read_csv(file_path)
    return accidents_depuis_1948


def get_city_weather_csv():
    file_path = os.path.join(
        cwd, 'fichiers_csv', "city_weather_visualcrossing.csv")
    city_weather_visualcrossing = pd.read_csv(file_path)
    return city_weather_visualcrossing


def get_flight_airlabs_mongo_db():
    # file_path = os.path.join(cwd, 'fichiers_csv', "flights_airlabs_12792.csv")
    # airlabs dataset
    # flight_airlabs = pd.read_csv(
    #     '/home/ubuntu/Main_Project_DE_Lufthansa_airlines/fichiers_csv/flights_airlabs_12792.csv', delimiter=',')
    flight_airlabs = get_airlabs_data()
    return flight_airlabs


def get_city_weather_api():
    file_path = os.path.join(
        cwd, 'fichiers_csv', "airports_lufthansa_11108.csv")
    airports_lufthansa = pd.read_csv(file_path)
    cities = airports_lufthansa['Nom Ville'].unique()
    df_weather= pd.DataFrame(columns = ['City', 'Description jour', 'Timezone', 'Latitude', 'Longitude', 'Date', 'Current time', 'Max_Température', 'Min_Température', 'Current temperature',
                                            'Humidité','Precipitation', 'Neige', 'Neige_densité', 'Vent_rafale', 'Vent_vitesse','Vent_direction', 'Pression', 'Nuage', 'Visibilité',
                                            'Solar radiation','Energy_solaire', 'Soleil_coucher', 'Alert risk','Description', 'Weather conditions', 'Weather alerts',
                                            'Alertes_description','Vitesse_vent'])
    c = 0
    for city_name in cities:
        if city_name == None: continue
        url= f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name.split('/')[0]}?unitGroup=metric&key={API_KEY_WEATHER}&contentType=json"
        resp2 = get(url)
        if resp2.status_code != 200:
            continue
        visual = resp2.json()
        c += 1
        if c%10 == 0: print(c)
        # try:
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
    df_weather.to_csv("city_weather_visualcrossing", index=False)
    return df_weather


def get_flight_airlabs_api():
    # return flight_airlabs
    try:
        flight_airlabs = get(f"http://0.0.0.0:8000/get_airlabs_data")
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
        print(flight_airlabs)
        insert_airlabs_data(flight_airlabs)
    except:
        flight_airlabs = get_flight_airlabs_mongo_db()
    return flight_airlabs
