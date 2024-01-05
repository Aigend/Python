#!/usr/bin/env bash

if [ ! -d "${PWD}/pb2/" ];then
    mkdir ${PWD}/pb2/
fi

protoc  -I ./protobuf/gb_db -I ./protobuf/custom -I ./protobuf/events  -I ./protobuf/periodical -I ./protobuf/base -I ./protobuf/rvs -I ./protobuf/nfc_key -I ./protobuf/adas -I ./protobuf/cdc --python_out ./pb2  ./protobuf/*/*.proto
touch ${PWD}/pb2/__init__.py
echo "VERSION = 17" > ./pb2/__init__.py
echo "compile successfully."