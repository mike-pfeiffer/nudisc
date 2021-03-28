FROM ubuntu:20.04

LABEL maintainer "Mike Pfeiffer <pfeiffermj@outlook.com>"

RUN apt-get update && \
    apt-get install -y python3 python3-pip nmap vim

RUN mkdir app && chmod 777 app && \
    mkdir app/discovery && chmod 777 app/discovery && \
    mkdir app/targets && chmod 777 app/targets

COPY ./app /app
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
