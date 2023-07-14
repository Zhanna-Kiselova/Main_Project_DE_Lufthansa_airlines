# We put this line below as a comment because this blocks the launching process 
# FROM debian:latest 
FROM python:3.9-slim-buster
# We install all the necessary libraries 
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests 
# Workdir - folder where is ou .py document
WORKDIR /folder_api/
# We add our .py document  
ADD helpers.py /folder_api/helpers.py
# Command to launch the .py document  
CMD python3 helpers.py