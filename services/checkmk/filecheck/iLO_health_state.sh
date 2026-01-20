#!/bin/bash

hosts='
192.168.15.121
192.168.15.122
192.168.15.123
'
# Clean previous content:
truncate -s 0 /var/cmk/iLO_state.csv
echo "Host,State" > /var/cmk/iLO_state.csv

for host in $hosts; do
    health=$(curl -s -k -u "$ILO_USER:$ILO_PASSWORD" https://$host/redfish/v1/Systems/1 | jq -r '.Status.Health')
    echo "$host,$health" >> /var/cmk/iLO_state.csv
done

