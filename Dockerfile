# syntax=docker/dockerfile:1
# Reference: https://docs.docker.com/compose/gettingstarted/

FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add build-base
RUN apk add --no-cache openssl-dev libffi-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
WORKDIR /code/src
CMD ["flask", "run"]
