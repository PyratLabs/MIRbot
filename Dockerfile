FROM python:3.5-alpine
MAINTAINER Xan Manning <git@xan-manning.co.uk>

RUN mkdir -p /app/mirbot
RUN mkdir -p /var/lib/mirbot

WORKDIR /app/mirbot
COPY . /app/mirbot

VOLUME /var/lib/mirbot

RUN pip3 install .

ENTRYPOINT [ "/app/mirbot/docker-entrypoint.sh" ]