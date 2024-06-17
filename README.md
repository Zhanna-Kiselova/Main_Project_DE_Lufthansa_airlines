# Main Project : "DST Lufthansa Airlines" 

Project summary : 

The main project as a result and final work of the data engineering learning program with the objective to expose the real-time international passenger flights on an interactive map. 

Utility of the project :

Personal ideas are welcome and the application also proposes some useful information about the current local weather as well as severe weather alerts worldwide in order to anticipate the planes flying over the dangerous zones, therefore avoiding or decreasing possible plane accidents.
Another part of the application will be dedicated to interactive data visualization through graphs and statistical dashboards. One of the statistics to present is about the airplane crashes. In order to propose maximum security and avoid any type of accidents, it is important to understand the cause of these consequences. This information can be interesting and be destinated to :

- passengers/clients to have a quick analysis on companies, which have the least/the most number of accidents and their analyse the causes 
- airline companies in order to better understand the problems of these accidents and take decisions for improvement.

Any exterior suggestions or remarks are more than welcome in order to improve this project. For any help or contact, don't hesitate to get in touch. 

This project can be cloned and run with docker-compose up in a terminal and can be visualized in the browser : 

- http://localhost:8050 (for Dash)
- http://localhost:8030 (for Fastapi)

Necessary requirements: 

For confidential purposes the personal credentials like token, passwords and the API_keys have not been disclosed. Therefore, you'll need to create your own accounts for :

- https://airlabs.co/
- https://www.visualcrossing.com/
- https://www.mapbox.com/maps 
- https://www.mongodb.com/

Please, note that due to a large volume of real-time data, the system imposes limitations and restrictions either in terms of API calls from extériour sites or in process running, resulting in slower outcome or difficulties to manage real-time big data. Because of limited resources, alternative options could not be considered. 

Be sure, to verify the necessary packages installation before launching the application. 

(Data Engineer course : promotion July, 2023/"Datascientest" learning center)








# Projet Fil Rouge "DST Lufthansa Airlines".

## 1. Introduction :

De nos jours, il est capable d’avoir des informations sur les vols dans le monde entier et de traquer en temps réel un avion. Nous pouvons observer ce site en guise d’exemple: https://www.flightradar24.com/48.73,2.28/6

Notre objectif est de s’y approcher le plus possible en passant par des API de différentes compagnies d’aviation. Dans notre cas ce seront les compagnies du groupe Lufthansa pour les vols commerciaux.

Pour personnaliser le projet et d'en tirer l'utilité, nous avons étudié différentes problématiques et nous avons défini un besoin réel. Il a été décidé de mettre les enjeux, telles que la sécurité du client/passager et la qualité du service proposé, au coeur de notre projet. Pour cela, nous avons opté pour les options d'analyses complémentaires, essentielles pour n'importe quelle compagnie aérienne grâce aux différentes API sollicitées telles que les alertes météo extrême pour la sécurisation des vols, statistiques sur les accidents aériens pour déterminer leur cause et permettre aux compagnies aériennes de faire les analyses nécessaires pour réduire au maximum les causes d'accidents et préserver les vies mais aussi d'éviter les possibles litiges et les frais liés à ces accidents pour pouvoir préserver également leur image etc.


## 2. Data :

Pour notre projet, nous avons principalement utilisé le site lufthansa mais nous étions libres d'utiliser toutes sources possibles pour la recherche d'informations. Voici, une liste non-exhaustive des sites utilisés pour la recherche :
- https://developer.lufthansa.com
- https://flightplandatabase.com/
- https://www.postman.com/
- https://www.iata.org/ 
- https://www.icao.int/ 
- https://airlabs.co/
- https://flightaware.com/
- https://opensky-network.org/
- https://datahub.io
- https://www.kaggle.com/
- https://en.wikipedia.org
- https://openweathermap.org/
- https://www.getambee.com/
- https://weatherstack.com/

Nous avons eu besoin principalement de la data suivante pour notre projet:
- vols en temps réel
- météo classique et alertes en temps réel
- aéroports
- villes
- pays  
- modèles avions
- statistiques sur les accidents de vols

## 3. Methodology :

Nous allons passer par 4 phases de notre projet Data:

- La collecte de la donnée : On va essayer d’extraire et réunir de la donnée pertinente au projet
- L’exploration de la donnée : On va essayer de comprendre la donnée qu’on a à disposition
- L’exploitation de la donnée : On va donner de la valeur à la donnée à disposition
- La mise en production : On va passer le projet à échelle

  
  3.1. LA COLLECTE DE LA DONNEE :

Pour la réalisation de n'importe quel projet, nous avons besoin d'avoir les données fiables de préférence obtenues des sources officielles.

Cela est possible grâce à une API (application programming interface). API - c'est un protocole de communication HTTP pour l'échange de données sur le Web. L'interrogation d'une API se fait avec l'aide d'une fonction get() du module requests qui nous permet de formuler une requête HTTP. Le résultat est stocké dans une variable. Si l'accès est autorisé, nous recevons un code 200 en vérifiant le status_code de notre variable. Pour meilleur visibilité et lisibilité, nous sauvegardons les données, qui ont été récupérées dans une vairable du format json() On peut également utiliser le site https://web.postman.co/ pour pouvoir visualiser les données au format json() de façon plus claire et pour savoir exactement quelles ressources on aura besoin de récupérer. La méthode la plus simple pour appeler une API est get() où l'on aura besoin de communiquer notre token pour pouvoir accéder aux données. La synthaxe obligatoire du site lufthansa exige de préciser le token présenté sous une variable "headers" et le lien de base doit être complété par une partie qui précise la source qui nous intéresse et pour laquelle nous faisons une requête. Nous sauvegardons encore une fois les données dans une variable qui sera sauvegardée au format json().

Pour qu'une API soit autorisée, nous aurons besoin de générer un token (authorisation du site).
Token est un code généré par le système API qui nous autorise de récupérer les informations qui ne sont pas "open-source".
Il y a plusieurs possibilités pour l'obtenir:

- via la commande curl/invité de commandes: curl "https://api.lufthansa.com/v1/oauth/token" -X POST -d "client_id=MY_ID" -d "client_secret=28QCGV8TjyuuMbctgvrJ" -d "grant_type=client_credentials"
- via Python : par la methode post ou get

Token a une durée limitée de 36h pour le site https://developer.lufthansa.com/page.

Si nous souhaitons, nous pouvons également automatiser le processus en créant une fonction.
Avant de lancer les opérations, il faut s'assurer si les packages nécessaires sont biens installés : package "requests" avec les méthodes post et get.

Si le module requests n'était pas installé, on devrait passer par :
- pip.exe install requests (pour Windows: Attention !!! Cette commande doit être exécutée en mode administrateur sous Windows, dans le menu Démarrer, clic droit sur l'application "invite de commandes" et choisir "exécuter en tant qu'administrateur".)
- pip3 install requests (sous Linux ou MacOS)

Pour info, l'extension est déjà installée sur VS Code. On ne fait que l'importer.


  3.2. L'EXPLORATION DE LA DONNEE :

Avant d'exploiter les données, nous avons besoin de les étudier. La meilleure façon de visualiser les données brutes récupérées au format csv ou json est via les dataframes ou les graphes. Cela nous permet de mieux comprendre les données et tirer l'essentiel de ces sources. Mais aussi de bien constater les erreurs eventuelles qui pourraient produire les faux résultats. 

Compte tenu du grand nombre des vols du groupe Lufthansa qui contient 7 compagnies aériennes, nous avons limité le nombre de résultats en se limitant à une seule date de départ et d'arrivée pour chaque compagnie.
Nous allons donc travailler avec les compagnies aériennes suivantes  :
- LH - Lufthansa
- EN - Air Dolomiti
- LX - Swiss
- OS - Austrian
- WK - Edelweiss
- SN - Brussels Airlines
- 4Y - Eurowings Discover

Nous avons l'autorisation suivante pour nos requêtes depuis les site lufthansa :
- 5	requetes/seconde
- 1.000 requetes/heure

Suite à cela, nous avons rencontré plusieurs difficultées avec les restrictions pour récupérer la data avec notre abonnement limité. Egalement, les datasets open-source récupérés depuis certains sites ne fournissaient pas les informations entièrement complètes. Les fichiers avaient besoin d'un grand travail de nettoyage (point à améliorer et prendre en considération car peu travaillé à cause de limite de temps).  

  3.3. L'EXPLOITATION DE LA DONNEE :

L'exploitation des données des vols en temps réel se fait directement en utilisant les documents json(), donc les données brutes en passant par les API. Ces documents sont stockés dans la base des données non-structurées/NoSQL, qui sont mieux adaptées pour la récupération des données que les BDD structurées/MySQL (souvent destinées aux analyses et études statistiques). Les BDD NoSQL proposent également la rapidité du traitement et d'intégration des données surtout dans notre étude de cas.

Logiquement, pour récupérer les données en temps réel nous n'avons pas besoin des les stocker car l'API va chercher directement ces informations et va les intégrer dans notre application. Mais, en cas d'imprévus ou des pannes informatiques des sites-sources, il est fortement conseillé d'avoir toujours un plan B, donc le stockage des données s'avère essentiel.

Egalement, dans le cadre de notre projet de fin d'études, nous souhaitions de montrer notre savoir-faire dans la création d'une architecture de pipeline de données qui est une tâche complexe et qui reste au coeur du métier de data engineer.

Compte tenu de besoins de notre projet, finalement nous avons fait un choix d'avoir un seul type de stockage (MongoDB/non-structurée même si initialement on a été partant pour les deux MongoDB/non-structurée et MySQL/structurée). MongoDB nous servira pour traiter les fichiers avec les données brutes, facile et rapide pour l'integration continue. Si notre projet viserait la partie destinée au service de ML pour les data scientists, la BDD MySQL aurait pu nous servir d'avoir les tables avec les données structurées pour pouvoir les explorer, faire les statistiques et les analyses plus poussées dans le Machine Learning et les modèles de prédiction (fichiers avec les données historiques sur les accidents d'avions et fichiers avec les données historiques météorologiques).


  3.4. LA MISE EN PRODUCTION :

Nous utiliserons enfin le module Dash de la librarie Python qui nous servira d'une interface de visualisation de notre application. Egalement pour intéragir avec l'utilisateur, nous allons créer les API callbacks/endpoints qui proposeront la direction vers les différentes pages de notre application. L'application sera sauvegardée dans un network unique avec plusieurs environnements dans un conteneur Docker et sera lancée avec la commande unique. Notre projet s'arrêtera là avec la présentation en live d'une apllication fonctionnelle ainsi d'un Power Point. Pour le déploiement permanent quand l'application serait améliorée et complétée d'avantage, on pourrait utiliser notre stockage des dossiers et fichiers sur GitHub qui propose les connexions nécessaires avec les outils clouds de différents providers, telles que AWS, Azure, GCP, etc.    

## 4. Résultats :

Proposition de l'application développée pourrait donner une idée pour l'élaboration plus sophistiquée. Cela pourrait être utile pour les individus (consultation personnelle) ainsi que pour les compagnies aériennes. Elle pourrait permettre de se concentrer sur les vols en temps réel et vérifier leurs status et les données complémentaires concernant chaque vol le jour-J. 

Les statistics sur les accidents enregistrés peuvent solliciter les compagnies aériennes de mener les actions nécessaires pour réduire les failles et les causes d'accidents mais également trouver des solutions durables pour l'avenir.

Les analyses sur la météo et les alertes peuvent donner la suite aux recherches plus poussées afin de comprendre comment réduire le nombre d'accidents en utilisant les prévisions, les prédictions et les alertes météo.
Mais également avec le rechauffement climatique, les données météorologiques peuvent être très utiles car elles sont liées directement au secteur aérien. L'air plus chaud, causé par les émissions de carbone, favorise les fortes turbulences. D’après les chiffres de l’ADEME, entre 1990 et 2019, les émissions de carbone du transport aérien ont augmenté de 85 %. Ainsi, en 2019, les émissions s’élevaient à 24,2 millions de tonnes de CO2. Cela représente l’équivalent de 5,3 % des émissions globales françaises - soit 2,2 fois plus qu’il y a 30 ans. 

Ce dérèglement climatique qui multiplie ces turbulences en avion qui ont augmenté de 50% en 40 ans. C'est surtout le cas quand on survole l'Atlantique, zone aérienne très fréquentée, où l'on est passé de 17 heures de fortes turbulences annuelles en 1979 à 27 heures en 2020. Des perturbations qui ne seraient pas sans incidence sur les avions. (source: étude menée par les chercheurs de l'université de Reading / Royaume-Uni et publiée dans la revue "Geophysical Research Letters"). Les possibles solutions pourraient peut-être proposées et étudiées : avion électrique, optimisation de ventes afin d'éviter les vols à moitité remplis, étude sur l'offre/demande de certaines destinations et/ou en périodes particulières, etc.   


## 5. Conclusion :

Proposition de l'application développée pourrait donner une idée pour l'élaboration plus sophistiquée. Cela pourrait être utile pour les individus (consultation personnelle) ainsi que pour les compagnies aériennes. Elle pourrait permettre de se concentrer sur les vols en temps réel et vérifier leurs statuts et les données complémentaires concernant chaque vol ainsi que les alertes météo le jour-J. 

Quelques idées pour aller plus loin et pour rendre cette solution plus intéressante :

- On pourrait pousser plus avant une étude sur le taux de remplissages des avions en vue d'optimiser la rentabilité et de réduire l'impact environnemental
- Il faudrait analyser de façon plus approfondie les causes des différents accidents aériens en tenant compte du plus grand nombre de facteurs pertinents afin de déterminer les mesures sécuritaires à prendre à l'avenir 
- Ce projet pourrait alors être un premier pas dans l'élaboration d'un projet collaboratif plus pointu en relation avec le développement durable et sécure
- On pourrait proposer des algorithmes de ML sur le comportement humain et prédictions d'erreurs
- Il serait intéressant de récupérer les alertes météo néfastes qui peuvent impacter la sécurité des vols (tremblement de terre, éruption de volcan, tsunami et ouragan en cas d'attérisage, tornades, foudre, etc).

D'un point de vue plus technique:

- Nous pourrions mettre au point un système d'automatisation (avec Airflow, par exemple) qui permettrait de mettre à jour régulièrement les  données non-statiques car un grand volume des données météo et des vols du jour demande un temps d'exécution assez fastidieux (en effectuant une nouvelle requête sur l'API des sites extérieurs et en remplaçant les données dans notre base de données)
- Egalement tout pourrait être orchestré par Kubernetes qui propose les ressources plus élaborées pour déployer une application et enfin la migration de l'infrastructure vers le cloud.

Les statistiques sur les accidents enregistrés peuvent solliciter les compagnies aériennes de mener les actions nécessaires pour réduire les failles et les causes d'accidents mais également trouver des solutions durables pour l'avenir.
Les analyses sur la météo et les alertes peuvent donner la suite aux recherches plus poussées afin de comprendre comment réduire le nombre d'accidents en utilisant les prévisions, les prédictions et les alertes météo.


Le projet a été conçu suite à la formation de data engineer proposée par "Datascientest". 

Paris, France
25.07.2023

https://medium.com/@zhannakiselova/projet-de-cr%C3%A9ation-dapplication-dst-lufthansa-airlines-5f0d8bc227e8

