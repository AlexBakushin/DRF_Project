FROM python:3

WORKDIR /app_drf

COPY ./requirements.txt /app_drf/

RUN pip install -r /app_drf/requirements.txt

COPY . .
