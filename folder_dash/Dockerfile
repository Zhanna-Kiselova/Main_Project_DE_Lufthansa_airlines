# We put this line below as a comment because this blocks the launching process 
# FROM debian:latest 
FROM python:3.9-slim-buster
# We install all the necessary libraries 
RUN apt-get update && apt-get install python3-pip -y && pip3 install dash
# Workdir - folder where is ou .py document
WORKDIR /folder_dash/
# We add our .py document  
ADD dash_app.py /folder_dash/dash_app.py
# We use the port 8050 for dash app
EXPOSE 8050
# Command to launch the .py document  
CMD python3 dash_app.py