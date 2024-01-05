#!/usr/bin/env python
# coding=utf-8
import json
import os
import requests
import yaml
import time

base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def evm_nofify_api(cmdopt, events):
    api = '/api/1/in/data/evm/notify'
    config_path = '{0}/config/{1}/{1}_config.yml'.format(base_dir, cmdopt)
    with open(config_path) as f:
        env_config = yaml.load(f)
    url = env_config['host']['tsp_in'] + api
    data = {
        "querystring": {
            "app_id": 10001,
            "lang": "zh-cn",
            "timestamp": round(time.time())
        },
        "payload": {
            "events": events
        },
        "headers": {
            "content-type": "application/x-www-form-urlencoded"
        },

    }
    data['payload']['events'] = json.dumps(data['payload']['events'])
    response = requests.request("POST", url, params=data['querystring'], data=data['payload'], headers=data['headers'])
    result = response.json()
    if result['result_code'] != 'success':
        assert False, "调用notify接口失败 {}".format(result)
    time.sleep(1)

