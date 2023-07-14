from pymongo import MongoClient
import pandas as pd
# package imports
import os
from dotenv import load_dotenv # pip install python-dotenv to be installed in the terminal 

cwd = os.getcwd()
dotenv_path = os.path.join(cwd, os.getenv('ENVIRONMENT_FILE', '.env'))
load_dotenv(dotenv_path=dotenv_path, override=True)

MONGO_URI = os.environ.get('mongo_db_uri')

client = MongoClient(
    MONGO_URI
)

# Creating a mongo database "lufthansa_database"
db = client["lufthansa_database"]

# Creating 6 collections to a mongo database "lufthansa_database"
airlabs_flights = db["airlabs_flights"]
visualcrossing_weather = db["visualcrossing_weather"]
lufthansa_schedule = db["lufthansa_schedule"]
countries_ourairports = db["countries_ourairports"]
airports_lufthansa = db["airports_lufthansa"]
airports_ourairports= db["airports_ourairports"]
aircrafts_wikipedia = db["aircrafts_wikipedia"]
accidents_kaggle = db["accidents_kaggle"]
aircrafts = db["crashes_kaggle"]

# BEFORE 
""" 
# Inserting real-time flights data into mongodb by deleting the previous one
def insert_airlabs_data(df):
    df_dict = df.to_dict(orient = 'records')
    airlabs_flights.delete_many({})
    airlabs_flights.insert_many(df_dict)

# Inserting real-time weather data into mongodb by deleting the previous one
def insert_weather_data(df):
    df_dict = df.to_dict(orient = 'records')
    visualcrossing_weather.delete_many({})
    visualcrossing_weather.insert_many(df_dict)

# Inserting airports data into mongodb from lufthansa_schedule.csv
def insert_schedule_data(df):
    lufthansa_schedule_dict = airports_lufthansa.to_dict(orient = 'records')
    lufthansa_schedule.insert_many(lufthansa_schedule_dict)

# Inserting airports data into mongodb from airports_lufthansa.csv
def insert_airports_lufthansa_data(df):
    lufthansa_airports_dict = airports_lufthansa.to_dict(orient = 'records')
    airports_lufthansa.insert_many(lufthansa_airports_dict)

# Inserting airports data into mongodb from airports_ourairports.csv
def insert_airports_ourairports_data(df):
    airports_ourairports_dict = airports_ourairports.to_dict(orient = 'records')
    airports_ourairports.insert_many(airports_ourairports_dict)

# Inserting countries data into mongodb from countries_ourairports.csv
def insert_countries_data(df):
    countries_dict = countries_ourairports.to_dict(orient = 'records')
    countries_ourairports.insert_many(countries_dict)
    
# Inserting accidents data into mongodb from accidents_kaggle.csv
def insert_accidents_data(df):
    accidents_dict = accidents_kaggle.to_dict(orient = 'records')
    accidents_kaggle.insert_many(accidents_dict)

# Inserting crashes data into mongodb from crashes_kaggle.csv
def insert_crashes_data(df):
    crashes_dict = crashes_kaggle.to_dict(orient = 'records')
    crashes_kaggle.insert_many(crashes_dict)

# Inserting aircrafts data into mongodb from aircrafts_wikipedia.csv
def insert_aircrafts_data(df):
    aircrafts_dict = aircrafts_wikipedia.to_dict(orient = 'records')
    aircrafts_wikipedia.insert_many(aircrafts_dict)



# Function get_airlabs_data() getting flights from the collection "airlabs_flights" of our mongo db "lufthansa_database", used by fastapi endpoints 
def get_airlabs_data():
    results = airlabs_flights.find()
    # data = list(results)
    # df = pd.DataFrame(data)
    return results


# Function get_weather_data() getting weather from the collection "visualcrossing_weather" of our mongo db "lufthansa_database", used by fastapi endpoints 
def get_weather_data():
    results = visualcrossing_weather.find()
    # data = list(results)
    # df = pd.DataFrame(data)
    return results

# Function get_airports_lufthansa_data() getting airports from the collection "airports_lufthansa" of our mongo db "lufthansa_database", used by fastapi endpoints 
def get_airports_data():
    results = airports_lufthansa.find()
    # data = list(results)
    # df = pd.DataFrame(data)
    return results

# Function get_countries_data() getting countries from the collection "countries_ourairports" of our mongo db "lufthansa_database", used by fastapi endpoints 
def get_countries_data():
    results = countries_ourairports.find()
    # data = list(results)
    # df = pd.DataFrame(data)
    return results

# Function get_accidents_data() getting accidents from the collection "accidents_kaggle" of our mongo db "lufthansa_database", used by fastapi endpoints 
def get_accidents_data():
    results = accidents_kaggle.find()
    # data = list(results)
    # df = pd.DataFrame(data)
    return results


# Function get_aircrafts_data() getting aircrafts from the collection "aircrafts_wikipedia" of our mongo db "lufthansa_database", used by fastapi endpoints 
def get_aircrafts_data():
    results = aircrafts_wikipedia.find()
    # data = list(results)
    # df = pd.DataFrame(data)
    return results

"""