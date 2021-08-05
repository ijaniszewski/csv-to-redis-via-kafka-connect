GOAL: Move data from given CSVs to Redis:
1. move data from CSVs to Kafka (via Kafka Connect)
2. move data from Kafka to Redis (via Kafka Connect)
3. Create scripts in python to query Redis

Solution should be provided as docker-compose.yml file with all necessary containers (Kafka, Kafka Connect, Redis)
<br><br>
<b>Solved:</b>
1. Start infrastructue - build images & run containers
```
docker-compose up
```

2. Deploy connectors on Kafka Connect Node
```
docker exec -it new_kafka_connect_infra_connect_1 bash deploy_connectors.sh
```

3. Check if there are keys in Redis
```
docker exec -it new_kafka_connect_infra_redis_1 redis-cli KEYS "movie-14*"
```

4. Run python script to check Movie ID in Redis database (use your own ID)
```
docker exec -it new_kafka_connect_infra_python_1 python get_data_from_redis.py --movie_id 1
```
<br><br>
Inspirations & sources:

[CSV SOURCE CONNECTOR](https://github.com/jcustenborder/kafka-connect-spooldir)

[CSV CONNECTOR WITH SCHEMA EXAMPLE](https://jcustenborder.github.io/kafka-connect-documentation/projects/kafka-connect-spooldir/sources/examples/SpoolDirCsvSourceConnector.schema.html)

[KAFKA INFRASTRUCTURE INSPIRATION](https://github.com/jcustenborder/kafka-connect-examples/blob/master/activemq-xml/docker-compose.yml)

[LOADING CSV TO KAFKA](https://rmoff.net/2020/06/17/loading-csv-data-into-kafka/)

[PASSWORDS IN A SEPARATE FILE](https://rmoff.net/2019/05/24/putting-kafka-connect-passwords-in-a-separate-file-/-externalising-secrets/)

<br><br>
Build & start containers
```
docker-compose up
```

check all installed Plugins on Kafka Connect Node
```
curl -s localhost:8083/connector-plugins|jq '.[].class'
```

Check if containers are running
```
docker container ps
```

connect to Kafka Broker
```
docker exec -it new_kafka_connect_infra_kafka_1 bash
```

check topics from Kafka Broker
```
kafka-topics --list --zookeeper zookeeper:2181
```

connect to Connect Node
```
docker exec -it new_kafka_connect_infra_connect_1 bash
```

check connectors
```
curl localhost:8083/connectors | jq .
```

check connector's status
```
connector_name=source_csv_comments_connector
curl localhost:8083/connectors/$connector_name/status | jq .
```

create connector
```
path_to_connector=/connectors/source_csv_comments_connector.json
curl -X POST -H "Content-Type: application/json" --data "@$path_to_connector" localhost:8083/connectors
```

update connector
```
path_to_connector=/connectors/source_csv_comments_connector.json
connector_name=source_csv_comments_connector
connector_config=$(jq -r '.config' $path_to_connector)
curl -X PUT -H "Content-Type: application/json" -d "${connector_config}" localhost:8083/connectors/$connector_name/config
```

delete connector
```
connector_name=source_csv_comments_connector
curl -X DELETE localhost:8083/connectors/$connector_name
```

check messages from Kafka Broker
```
topic=comments
kafka-console-consumer --bootstrap-server localhost:9092 --topic $topic --from-beginning --max-messages 5
```

check Kafka Topic deserialized in Avro (from Kafka Connect Node)
```
topic=comments
kafka-avro-console-consumer --topic $topic --property schema.registry.url=http://schema-registry:8081 --bootstrap-server kafka:9092 --from-beginning --max-messages 5
```

remove all stopped containers
```
docker container prune
```

remove docker image
```
docker image rm new_kafka_connect_infra_connect
```

remove all docker volumes
```
docker volume rm $(docker volume ls -q)
```

connect to Redis Node
```
docker exec -it new_kafka_connect_infra_redis_1 redis-cli
```

check Redis Keys
```
KEYS movie-*
```

Count number of elements in Redis Set
```
ZCOUNT id_movie-1 -inf +inf
```

Get value based on Redis Key
```
GET movie-1
```

Get elements from Redis Set
```
ZRANGE id_movie-1 0 -1
```
