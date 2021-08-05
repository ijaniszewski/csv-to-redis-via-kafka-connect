FROM python:3.9.2
RUN apt-get update \
    && apt-get install -y vim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt