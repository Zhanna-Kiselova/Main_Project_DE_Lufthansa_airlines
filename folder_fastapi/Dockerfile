# We put this line below as a comment because this blocks the launching process 
# FROM debian:latest 
FROM python:3.9-slim-buster
# We install all the necessary libraries 
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install fastapi
# Workdir - folder where is ou .py document
WORKDIR /folder_fastapi/
# We add our .py document  
ADD fast_api_endpoints.py /folder_fastapi/fast_api_endpoints.py
# We use the port 8000 for fastapi endpoints
EXPOSE 8000
# Command to launch the .py document  
CMD python3 fast_api_endpoints.py