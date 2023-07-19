# package imports
import os # to manage the subfiles and find files easier 
from dotenv import load_dotenv # reads key-value pairs from a .env file and can set them as environment variables
# pip install python-dotenv to be installed in the terminal ubuntu for environmental variables 

cwd = os.getcwd()  # varibale for defining the current working directory 
dotenv_path = os.path.join(cwd, os.getenv('ENVIRONMENT_FILE', '.env')) # variable to find the path to the directory with the file and the environmental variables
load_dotenv(dotenv_path=dotenv_path, override=True)  

AIRLABS_API_KEY = os.environ.get('api_key_airlabs') # new variable for the airlabs key value, taken from the environmental variable in setting.py
API_KEY_WEATHER = os.environ.get('api_key_weather') # new variable for the weather key value, taken from the environmental variable in setting.py
API_KEY_MAPBOX = os.environ.get('api_key_mapbox') # new variable for the mapbox key value, taken from the environmental variable in setting.py