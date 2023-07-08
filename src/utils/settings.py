# package imports
import os
from dotenv import load_dotenv # pip install python-dotenv to be installed in the terminal 

cwd = os.getcwd()
dotenv_path = os.path.join(cwd, os.getenv('ENVIRONMENT_FILE', '.env'))
load_dotenv(dotenv_path=dotenv_path, override=True)

# AIRLABS_API_KEY = os.environ.get('api_key_airlabs')
API_KEY_WEATHER = os.environ.get('api_key_weather')
API_KEY_MAPBOX = os.environ.get('api_key_mapbox')
MONGO_URI = os.environ.get('mongo_db_uri')