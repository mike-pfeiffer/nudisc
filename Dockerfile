FROM ubuntu:20.04

LABEL maintainer "Mike Pfeiffer <pfeiffermj@outlook.com>"

ENV TIME_ZONE=Etc/GMT

RUN ln -snf /usr/share/zoneinfo/$TIME_ZONE /etc/localtime && printf $TIME_ZONE > /etc/timezone

RUN apt-get update && \
    apt-get install -y python3 python3-pip nmap vim nginx uwsgi supervisor

RUN mkdir app && chmod 777 app && \
    mkdir app/discovery && chmod 777 app/discovery && \
    mkdir app/targets && chmod 777 app/targets

COPY ./app /app
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 80/tcp
CMD ["nginx", "-g", "daemon off;"]
