#!/bin/bash

STATION=$1
FILE=$2

echo "upload file: ${FILE} to station: ${STATION}"

python3 vpn_jump.py scp download ${STATION} ${FILE}
