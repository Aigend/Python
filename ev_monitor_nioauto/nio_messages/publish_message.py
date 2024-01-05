#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/06/24 18:40
@contact: hongzhen.bi@nio.com
@description: 上报数据
"""
import importlib
import logging
import os
import random
import string
import time

from .utils.commonlib import show_json
from .utils.kafka_client import KafkaProduct
from .utils import httptool as req
from .utils.mqtt_client import MqttClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))



def publish_msg_by_mqtt(event_name, vid, vin, env='test', sleep_time=2, *args, **kwargs):
    module = importlib.import_module('nio_messages.' + event_name, ".")
    gen_function = getattr(module, "generate_message")
    nextev_message, obj = gen_function(vin, vid, *args, **kwargs)

    client_id = _get_client_id(env, vid)
    cert_path = '{0}/config/{1}/{2}/'.format(BASE_DIR, env, vid)
    if not os.path.exists(cert_path):
        _download_cert(env, vid)
    client = MqttClient(client_id,
                        cert_path + "ca/tls_tsp_trustchain.pem",
                        cert_path + "client/tls_lion_cert.pem",
                        cert_path + "client/tls_lion_priv_key.pem")
    host = f"tsp-nmp-{env}.nioint.com"
    port = 20083
    client.connect(host, port, 20)
    client.loop_start()
    client.publish(bytearray(nextev_message))
    logging.info("Generated {} message and publish by mqtt:\n{}".format(event_name, show_json(obj)))
    time.sleep(sleep_time)
    client.loop_stop()
    client.disconnect()
    return nextev_message, obj


def publish_msg_by_kafka(event_name, vid, vin, env='test', sleep_time=2, *args, **kwargs):
    """
    当用消息平台上报时，accound_id所对应的vid不重要，tsp会通过证书自动填写对应的vid，但是通过kafka上报时，vid必须填写正确
    """
    module = importlib.import_module('nio_messages.' + event_name, ".")
    gen_function = getattr(module, "generate_message")

    nextev_message, obj = gen_function(vin, vid, *args, **kwargs)

    kafka = KafkaProduct()
    if env == 'test':
        kafka.product({
            'bootstrap.servers': 'cvs-kafka-test.nioint.com:39093',
            'group.id': 'ev_monitor_test',
            'auto.offset.reset': 'latest',
            'sasl.username': '5NEgo3WTBXme',
            'sasl.password': 'EJ4XPXviukTv',
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'sasl_plaintext',
        })
        kafka.send('swc-cvs-nmp-test_tsp-10005-data_report', nextev_message)
    elif env == 'stg':
        kafka.product({
            'bootstrap.servers': ','.join(['cvs-kafka01-stg.nioint.com:9092', 'cvs-kafka02-stg.nioint.com:9092', 'cvs-kafka03-stg.nioint.com:9092']),
            'group.id': 'ev_monitor_test',
            'auto.offset.reset': 'latest',
            'sasl.username': 'mv5ET4yB379G',
            'sasl.password': 'X84vUQotCzNT',
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'sasl_plaintext',
        })
        kafka.send('swc-cvs-nmp-stg_tsp-10005-data_report', nextev_message)
    else:
        logging.error('Wrong environment')

    logging.info("Generated {} message and publish by kafka:\n{}".format(event_name, show_json(obj)))

    time.sleep(sleep_time)

    return nextev_message, obj


def _download_cert(env, vid):
    ca_path = os.path.join(BASE_DIR, "config", env, vid, "ca")
    client_path = os.path.join(BASE_DIR, "config", env, vid, "client")
    if not os.path.exists(ca_path):
        os.makedirs(ca_path)
    if not os.path.exists(client_path):
        os.makedirs(client_path)

    host = f'https://tsp-{env}-int.nio.com'
    url = f"{host}/api/1/in/vehicle/{vid}/certs"
    data = {'types': ['lion', 'airbender', 'asimov']}
    params = {'app_id': '10016'}
    token = _refresh_token(env)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        "Authorization": token
    }
    try:
        r = req.request("POST", url, data=data, headers=headers, params=params, timeout=5.0)
        if r.status_code != 200:
            raise Exception(f"Request error! Status code:{r.status_code}")
        response = r.json()

        cert_chain = ca_path + os.sep + 'tls_tsp_trustchain.pem'
        with open(cert_chain, 'w') as f:
            f.write(response['data']['trust_chain'])
        for key in response['data']:
            if "key" in key or 'cert' in key:
                cert_file = client_path + os.sep + key + '.pem'
                with open(cert_file, 'w') as f:
                    f.write(response['data'][key])
    except Exception:
        raise Exception("Error: 没有找到这辆车的证书文件，检查一下车辆环境或者vid是否正确")


def _refresh_token(env):
    account = {
        "test": {"mobile": 98762751022, "vc_code": 413692},
        "stg": {"mobile": 98762485616, "vc_code": 842937},
        "dev": {"mobile": 98762427419, "vc_code": 627139}
    }
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
               }
    url = f'https://app-{env}.nio.com/acc/2/login'
    params = {
        'region': 'cn',
        'lang': 'zh-cn',
        'app_id': '10001',
        'nonce': 'abcdefefef' + random.choice(string.ascii_letters)
    }
    data = {
        'mobile': account[env]["mobile"],
        'verification_code': account[env]["vc_code"],
        'country_code': '86',
        'authentication_type': 'mobile_verification_code',
        'device_id': 'adnkjadfnvcnak',
        "terminal": '{"name":"我的华为手机","model":"HUAWEI P10"}',
    }
    res = req.request('POST', url=url, headers=headers, params=params, data=data).json()
    if res.get('result_code') == 'success':
        return 'Bearer ' + res['data']['access_token']
    else:
        raise Exception("Failed to refresh access token")
    
    
def _get_client_id(env, vid):
    appid = '10005'
    url = f'https://tsp-{env}.nio.com'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close'
    }
    data = {
        'app_version': '1.3.4',
        'brand': 'xiaomi',
        'device_type': 'vehicle',
        'device_token': 'def12131414g1423fff',
        'device_id': vid,
        'os': 'android',
        'os_version': '6.0',
        'nonce': 'randomstring1'
    }
    params = {
        'lang': 'zh_CN',
        'region': 'CN',
        'app_id': appid
    }
    api = '/api/1/message/register_client'
    res = req.request('POST', url=url + api, params=params, data=data, headers=headers, timeout=5.0)
    res_json = res.json()
    if res_json['result_code'] == 'success':
        return res_json['data']['client_id']
    else:
        raise Exception("client_id注册失败")
