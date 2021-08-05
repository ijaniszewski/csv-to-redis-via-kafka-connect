for connector in /connectors/*.json
    do 
        curl -X POST -H "Content-Type: application/json" --data "@$connector" localhost:8083/connectors
        connector_name=$(jq -r '.name' $connector)
        echo "$connector_name deployed"
    done