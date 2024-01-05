#!/bin/bash

RESOURCE_ID=$1
echo "connect to station: ${RESOURCE_ID}"

python3 vpn_jump_opman.py ssh ${RESOURCE_ID}