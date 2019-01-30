#!/bin/bash
#script to get public ip address
# /usr/local/bin/getpublicip.sh

echo "PUBLICIP=$(curl -vv ipinfo.io/ip 2> /run/publicip.log)\n" > /run/publicip;
sleep 600