#!/bin/bash

if [ ! -n "$1" ];then
    echo "please make command like ./pslog.sh [resource id] [mounth] [day] [hour]"
    exit 0
fi

RESOURCE=$1
MOUNTH=$2
DAY=$3
HOUR=$4

SAVE_PATH=`date +%Y-%m-%d-%H-%M-%S`
mkdir -p  ${HOME}/vpn/log/${SAVE_PATH}

echo "download ing, please wait a few seconds ..."
python3 vpn_jump_opman.py scp download ${RESOURCE} "/warehouse/log/PS/2023-$MOUNTH-$DAY.$HOUR*"

echo "save log to: ${HOME}/vpn/log/$SAVE_PATH"
mv 2023-$MOUNTH-$DAY.$HOUR* ${HOME}/vpn/log/${SAVE_PATH}
sync
sync

echo "download log finish!!!"
echo "download log finish!!!"
