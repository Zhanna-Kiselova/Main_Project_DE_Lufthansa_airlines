from fastapi import FastAPI
from requests import get
import uvicorn
import pandas as pd
import os
from dotenv import load_dotenv # pip install python-dotenv to be installed in the terminal 
from fastapi.responses import JSONResponse
import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from markupsafe import Markup
from pymongo import MongoClient
import pandas as pd
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


api=FastAPI()

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    correct_username = "datascientest"
    correct_password = "datascientest"
    if username == correct_username and password == correct_password:
        return username
    raise HTTPException(status_code=401, detail="Incorrect credentials")

@api.get("/")
def get_index():
    return "Welcome. This is the application API page. You'll have to enter the username and a password in order to get the data at this endpoint: /authorization. The username and the password are the same and both correpond to a name of the data learning center for which this application has been done (in small caps). If successful, you'll be able to get real-time flights data"

@api.get("/authorization")
def get_authorization(username: str = Depends(get_current_username)):
    authorization_text = ''' - to get flights status data, go to this endpoint after the main link base: /get_flights_data<br>
- to get weather status data, go to this endpoint after the main link base: /get_weather_data<br>
- to get airports data, go to this endpoint after the main link base: /get_airports_data<br>
- to get countries data, go to this endpoint after the main link base: /get_countries_data<br>
- to get aircrafts data, go to this endpoint after the main link base: /get_aircrafts_data<br>
- to get accidents data, go to this endpoint after the main link base: /get_accidents_data<br>
'''
    return HTMLResponse(content=Markup(authorization_text))


# Inserting airlabs data into mongodb using fastapi endpoint (!!!!!!! betther transfer flights data into .json from api requests and put directly to mongo and delete this endpoint)
@api.put("/insert_airlabs_data")  
def insert_airlabs(dataframe: dict):
    data = dataframe['data']
    data = json.loads(data)
    df = pd.DataFrame(data)
    df_dict = df.to_dict(orient = 'records')
    airlabs_flights.delete_many({})
    airlabs_flights.insert_many(df_dict)
    return {"message" : "data inserted"}


@api.put("/insert_weather_data")
def insert_weather(dataframe: dict):
    data = dataframe['data']
    data = json.loads(data)
    df = pd.DataFrame(data)
    print(df)
    df_dict = df.to_dict(orient = 'records')
    visualcrossing_weather.delete_many({})
    visualcrossing_weather.insert_many(df_dict)
    return {"message" : "data inserted"}

# API endpoint for the Dash application, getting airlabs flights from mongo_database.py function get_airlabs_data()
@api.get("/get_flights_data") # Changed for /get_flights_data instead of /get_airlabs_data 
def get_airlabs():
    results = airlabs_flights.find()
    records = list(results)
    return json.dumps(records, default=str)


# API endpoint for the Dash application, getting visualcrossing weather from mongo_database.py using function get_weather_data() from mongo_database.py 
@api.get("/get_weather_data")
def get_weather():
    results = visualcrossing_weather.find()
    records = list(results)
    return json.dumps(records, default=str)


# API endpoint for the Dash application, getting airports_lufthansa from mongo_database.py using function get_airports_data() from mongo_database.py
@api.get("/get_airports_data")
def get_airports():
    results = airports_lufthansa.find()
    records = list(results)
    return json.dumps(records, default=str)


# API endpoint for the Dash application, getting countries from mongo_database.py function get_countries_data()
@api.get("/get_countries_data")
def get_countries():
    results = countries_ourairports.find()
    records = list(results)
    return json.dumps(records, default=str)

# API endpoint for the Dash application, getting aircrafts from mongo_database.py function get_aircrafts_data()
@api.get("/get_aircrafts_data")
def get_aircrafts():
    results = aircrafts_wikipedia.find()
    records = list(results)
    return json.dumps(records, default=str)

# API endpoint for the Dash application, getting accidents from mongo_database.py function get_accidents_data()
@api.get("/get_accidents_data")
def get_accidents():
    results = accidents_kaggle.find()
    records = list(results)
    return json.dumps(records, default=str)


if __name__ == "__main__":
    uvicorn.run(api, host="localhost", port=8000)