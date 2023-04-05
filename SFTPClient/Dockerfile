FROM ubuntu:latest

RUN apt update

WORKDIR /usr/app/src

RUN apt-get install nano -y
RUN apt install python3 -y
RUN apt-get install python3 pip -y
RUN pip install paramiko
RUN apt-get install cron -y

COPY . ./

