from fastapi import FastAPI
from requests import get
import uvicorn
import pandas as pd
import os
from dotenv import load_dotenv # pip install python-dotenv to be installed in the terminal 
from fastapi.responses import JSONResponse

cwd = os.getcwd()
dotenv_path = os.path.join(cwd, os.getenv('ENVIRONMENT_FILE', '.env'))
load_dotenv(dotenv_path=dotenv_path, override=True)

AIRLABS_API_KEY = os.environ.get('api_key_airlabs')
API_KEY_WEATHER = os.environ.get('api_key_weather')


api=FastAPI()

@api.get('/')
def get_index():
    return 'welcome' 

@api.get("/get_airlabs_data")
def get_flight_airlabs_data():
    flight_airlabs = get(f"https://airlabs.co/api/v9/flights?api_key={AIRLABS_API_KEY}")
    flight_airlabs = flight_airlabs.json()
    return flight_airlabs


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)