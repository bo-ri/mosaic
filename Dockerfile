FROM python:3.6.0

RUN apt-get update -y && apt-get upgrade -y

RUN pip install pillow numpy matplotlib pymongo glob