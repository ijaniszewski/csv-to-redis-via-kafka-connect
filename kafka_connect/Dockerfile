FROM confluentinc/cp-kafka-connect:5.5.3

# Copying Redis Sink Connector
RUN mkdir -p /usr/share/redis-sink
COPY kafka-connect-redis-1.2.2-2.1.0-all.jar /usr/share/redis-sink/

# Installing the Spool Dir Connector
RUN confluent-hub install --no-prompt jcustenborder/kafka-connect-spooldir:latest

RUN apt-get update \
    && apt-get install -y vim jq

# Copy credentials - just to show how it works, don't do it that way on PROD!
COPY credentials.properties credentials.properties

# Copy script to deploy connectors
COPY deploy_connectors.sh deploy_connectors.sh
