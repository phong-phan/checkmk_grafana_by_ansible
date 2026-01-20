#!/bin/bash

hosts='
192.168.15.121
192.168.15.122
192.168.15.123
'
for host in $hosts
do
	# Clean previous content for each file:
	truncate -s 0 /var/cmk/$host.csv
	echo 'Component,State' > /var/cmk/$host.csv
	curl -s -k -u "$ILO_USER:$ILO_PASSWORD" https://$host/redfish/v1/Systems/1 | jq -r '
	  .Oem.Hpe.AggregateHealthStatus |
	  to_entries[] |
	  select(.value.Status?.Health) |
	  "\(.key),\(.value.Status.Health)"
	' >> /var/cmk/$host.csv
done
