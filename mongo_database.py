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

db = client["lufthansa_database"]
airlabs_flights = db["airlabs_flights"]

def insert_airlabs_data(df):
    df_dict = df.to_dict(orient = 'records')
    airlabs_flights.delete_many({})
    airlabs_flights.insert_many(df_dict)

def get_airlabs_data():
    results = airlabs_flights.find()
    # data = list(results)
    # df = pd.DataFrame(data)
    return results

