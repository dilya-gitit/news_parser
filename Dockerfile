FROM python:3.12.0a7-bullseye

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt