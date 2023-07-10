from fastapi import FastAPI
from requests import get
import uvicorn
import pandas as pd
import os
from dotenv import load_dotenv # pip install python-dotenv to be installed in the terminal 
from fastapi.responses import JSONResponse
import json

from mongo_database import insert_airlabs_data, get_airlabs_data



api=FastAPI()

@api.get('/')
def get_index():
    return 'welcome' 

@api.put("/insert_airlabs_data")
def insert_airlabs(dataframe: dict):
    data = dataframe['data']
    data = json.loads(data)
    df = pd.DataFrame(data)
    insert_airlabs_data(df)
    return {"message" : "data inserted"}

@api.get("/get_airlabs_data")
def get_airlabs():
    records = get_airlabs_data()
    records = list(records)
    return json.dumps(records, default=str)


if __name__ == "__main__":
    uvicorn.run(api, host="localhost", port=8000)