FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=reservations.settings.dev

RUN mkdir /app
WORKDIR /app

ADD . /app/

RUN apt-get update \
&& apt-get install -y vim vim-nox

RUN pip install --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt
