# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author:rosa.xiao
# @Time:2023/12/1 20:48
# @File: oss_utils.py
import time
import requests
import json
from utils.log import log

def generateVirtualKey(req_body):
    """

    :param :
    :param :
    :param :
    :return:
    """
    oss_generate_VirtualKey_url = "http://pow-oss-stg.nioint.com/v1/credentials/generateVirtualKey"
    header = {
        "content-type": "application/json"
    }
    req_body = json.dumps(req_body)
    respose = requests.post(oss_generate_VirtualKey_url, data=req_body, headers=header)
    respose_json = respose.json()
    return respose_json

def remote_control(station_id,req_body):
    """
    :param :
    :param :
    :param :
    :return:
    """
    ability_operates = req_body.get("ability_operates")
    ability_operates_0 = ability_operates[0]
    ability_code = ability_operates_0.get("ability_code")
    log.info(f"<remote control><cmd>: {ability_code}")
    remote_control_url = f"http://pow-stg.nioint.com/pe/prime/platform/v1/device-ability/remote-control/{station_id}?app_id=100456"
    if ability_code == "order_notify" or ability_code == "shutter_door_control":
        remote_control_url = f"http://pow-stg.nioint.com/pe/prime/platform/v1/device-ability/remote-control/{station_id}?app_id=100036"
    headers = {
        "content-type": "application/json",
        "X-User-ID": "mini.ye",
        "X-User-Type": "NIO_ACCOUNT"
    }
    req_body = json.dumps(req_body)
    log.info(f"<device><req>: {req_body}")
    respose = requests.post(remote_control_url, data=req_body, headers=headers)
    respose_json = respose.json()
    log.info(f"<oss><rep>: {respose_json}")
    return respose_json

if __name__ == '__main__':
    pass