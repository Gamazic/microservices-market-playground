FROM python:3.10-slim-buster

RUN apt-get update && apt-get install libpq-dev python3-dev curl -y

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN opentelemetry-bootstrap -a install

COPY . .
