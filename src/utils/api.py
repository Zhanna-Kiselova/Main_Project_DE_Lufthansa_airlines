
# Imports des librairies nécessaires
import requests
import os # to launch easily from another localhost
from requests import post, get
import pandas as pd
from time import sleep, time
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys # to check the version of python
import json

# Génération d'un nouveau token par Python (notre client_id et client_secret nous ont été communiqués lors de l'inscription sur le site lufthansa.com. Ces identifiants sont confidentiels et uniques à chaque utilisateur
# et doivent être sauvegardés)
reponse = post("https://api.lufthansa.com/v1/oauth/token", data = {'client_id':'69chxjbxs3mwe34sgn5hmm62', 'client_secret':'28QCGV8TjyuuMbctgvrJ', 'grant_type':'client_credentials'})
reponse.text

# Nous récupérons les informations sur le token au format .json
reponse.json()
print(reponse)

# Nous attribuons le token généré à une variable token
key = reponse.json()['access_token']
token = {"Authorization": "Bearer" + ' ' + key}
token
print(token)


# Nous souhaitons faire une requête pour pouvoir visualiser de façon claire ces compagnies ainsi que les détails des vols
# Nous utilisons la base du lien https://api.lufthansa.com/v1 que nous compléterons par l'information dont on a besoin. Ici on récupère les informations sur codes des compagnies aériennes du groupe Lufthansa (7 airlines)
# Nous créons un dataframe avec tous les vols du groupe Lufthansa sous une variable "df_all".
companies=['LX', 'LH', 'EN', 'OS', 'WK', 'SN', '4Y']
date=datetime.now().strftime("%d%b%y").upper()
dict_companies = {}
df_all = pd.DataFrame()
for company in companies:
  resp = get(f"https://api.lufthansa.com/v1/flight-schedules/flightschedules/passenger?airlines={company}&startDate={date}&endDate={date}&daysOfOperation=1234567&timeMode=UTC", headers = token)
  sleep(1)
  if resp.status_code != 200: continue
  print(company)
  response = resp.json()
  # On crée le DataFrame pour visualiser les informations sur LH
  df = pd.DataFrame([[response[n]['airline'], response[n]['flightNumber'],
                      response[n]['legs'][0]['origin'], response[n]['legs'][0]['destination'], response[n]['legs'][0]['aircraftType'], response[n]['legs'][0]['op'],
                      response[n]['periodOfOperationUTC']['startDate'], response[n]['periodOfOperationLT']['startDate'], response[n]['periodOfOperationUTC']['endDate'], response[n]['periodOfOperationLT']['endDate'],
                      response[n]['legs'][0]['aircraftDepartureTimeUTC'], response[n]['legs'][0]['aircraftDepartureTimeLT'], response[n]['legs'][0]['aircraftArrivalTimeUTC'], response[n]['legs'][0]['aircraftArrivalTimeLT']]
                      for n in range(len(response))],
                      columns = ["Compagnie", "Numéro de vol", "Lieu de départ IATA", "Lieu d'arrivée IATA", "Aircraft Code IATA",
                                "Opérationnel", "Date départ UTC", "Date départ LT", "Date arrivée UTC", "Date arrivée LT", "Heure départ (en min UTC)", "Heure départ (en min LT)", "Heure arrivée (en min UTC)", "Heure arrivée (en min LT)"])
  dict_companies[company] = df
  df_all = pd.concat([df_all, df], axis=0)
print(len(df_all))
print(df_all)
