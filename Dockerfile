FROM python:latest

WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt
COPY . /src
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
