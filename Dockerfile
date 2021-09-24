#Create a Debian-Jessie base image with python 3.6.9 installed.
FROM python:3.6.9-slim-jessie

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set display port as an environment variable
ENV DISPLAY=:99

#Update package-list
RUN apt-get update

#Install tar
RUN apt-get install --no-install-recommends -yqq tar

#Install firefox
RUN apt-get install --no-install-recommends -yqq firefox-esr

#Install wget
RUN apt-get install --no-install-recommends -yqq wget

#Download Firefox Geckodriver Linux 
RUN wget -O /tmp/geckodriver-v0.29.1-linux64.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz

#Unzip Firefox Geckodriver Linux.tar.gz
RUN tar -xvzf /tmp/geckodriver-v0.29.1-linux64.tar.gz 

#Remove Firefox Geckodriver Linux.tar.gz
RUN rm /tmp/geckodriver-v0.29.1-linux64.tar.gz

#Move Firefox Geckodriver Linux in Path 
RUN mv geckodriver /usr/local/bin/

#Apt-get clean and autoclean
RUN apt-get clean && apt-get autoclean

#Pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

#Directory
WORKDIR /app
COPY . /app

#Create a volume
VOLUME /data

#Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

#Port the access
EXPOSE 5000

#Running the flask-Server
ENV FLASK_APP=Pages.py

ENV FLASK_ENV=development

CMD ["flask", "run", "--host", "0.0.0.0"]