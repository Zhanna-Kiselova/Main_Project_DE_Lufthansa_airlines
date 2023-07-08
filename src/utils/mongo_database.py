from pymongo import MongoClient
import pandas as pd
 
# local imports
from .settings import MONGO_URI

client = MongoClient(
    MONGO_URI
)

db = client["lufthansa_database"]
airlabs_flights = db["airlabs_flights"]

def insert_airlabs_data(df):
    df_dict = df.to_dict(orient = 'records')
    airlabs_flights.delete_many({})
    airlabs_flights.insert_many(df_dict)

def get_airlabs_data():
    results = airlabs_flights.find()
    data = list(results)
    df = pd.DataFrame(data)
    return df
