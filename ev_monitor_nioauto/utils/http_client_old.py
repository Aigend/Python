#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:chunming.liu
@time: 2020/06/16 16:38
@contact: chunming.liu@nio.com
@description: 发起http请求的客户端，封装了requests，根据tsp的业务场景增加了变量替换、自动签名、证书查找、自动代理等功能
"""
import json
from utils.logger import logger as logging
# import logging
import os
from json import JSONDecodeError

import allure
import curlify
import requests
from urllib3 import encode_multipart_formdata

from utils.encryption import rsa, sha3256, get_encryption, des3_encrypt
from utils.signature import moatkeeper_signature


class TSPRequest(object):
    @staticmethod
    def request(env, inputs):
        # 1. 用配置文件中的数据替换测试数据中{{}}中间的内容
        # inputs = render(env, inputs) # 放到pytest_generate_tests中了
        cmdopt = env['cmdopt']
        # inputs = format(inputs)

        if 'marcopolo' in cmdopt and 'params' in inputs and 'sign' in inputs['params']:
            if int(inputs['params']['app_id']) < 1000000:
                inputs['params']['hash_type'] = 'sha256'
                app_id_map = {'10000': 10000, '10001': 1000004, '10002': 1000003, '10003': 1000014, '10004': 10004,
                              '10005': 10005, '10006': 1000027, '10007': 10007, '10014': 1000012, '10018': 1000014,
                              '30006': 30006, '30007': 30007, '80001': 80001, '80002': 80002, '10016': 10000, "10022": 10022,
                              '100423': 100423,
                              }
                try:
                    if "data" in inputs and "origin_app_id" in inputs["data"]:
                        inputs['data']['origin_app_id'] = app_id_map[str(inputs['data']['origin_app_id'])]
                    inputs['params']['app_id'] = app_id_map[str(inputs['params']['app_id'])]
                except Exception:
                    logging.error(f"{str(inputs['params']['app_id'])} not found in map")
                    return f"内部错误，app_id {str(inputs['params']['app_id'])} error"

        # 2. 加密pin_code和密码
        encode_pincode(env, inputs)
        encode_password(env, inputs)

        # 3. 计算签名，并添加到params
        if 'params' in inputs and 'sign' in inputs['params']:
            headers = inputs.get('headers')
            token = None
            if headers:
                token = headers.get('Authorization')
            sign = moatkeeper_signature(inputs.get('method'),
                                        inputs.get('path'),
                                        inputs.get('params'),
                                        inputs.get('data'),
                                        inputs.get('json'),
                                        env['secret'][int(inputs["params"]["app_id"])],
                                        token)
            inputs['params']["sign"] = sign

        # 4. 设置代理，命令行如何设置代理的话，就走代理
        if env.get('proxy'):
            inputs['proxies'] = env.get('proxies')

        # 5. 发送请求
        # logging.info("请求对象\n" + json.dumps(inputs, indent=2, ensure_ascii=False))
        with allure.step("发起请求{}{}".format(inputs.get("method"), inputs.get("host") + inputs.get("path"))):
            # allure.attach(json.dumps(inputs, indent=2, ensure_ascii=False), '请求对象')
            r = requests.request(inputs.pop("method"),
                                 url=inputs.pop("host") + inputs.pop("path"),
                                 **inputs)
            curl_print(r.request, inputs)
            r.encoding = 'utf-8'
            try:
                response = r.json()
                response_txt = json.dumps(response, indent=2, ensure_ascii=False)
            except JSONDecodeError:
                response = response_txt = r.text
            allure.attach(response_txt, '响应结果')
            logging.info("响应结果\n" + response_txt)
            return response


def curl_print(req: requests.request, inputs):
    curl_str = curlify.to_curl(req)

    if 'cert' in inputs and inputs['cert'] is not None:
        curl_str += f" --tlsv1.2 --cert {inputs['cert'][0]} --key {inputs['cert'][1]}"
        curl_str += f" --cacert {inputs['verify']}" if 'verify' in inputs else " -k"

    logging.info(curl_str)


def encode_pincode(env, inputs):
    if inputs.get('data', False) and 'pin_code' in inputs['data']:
        key_id, key = get_encryption(env, inputs['params']['app_id'])
        inputs['data']['pin_code'] = rsa(sha3256(inputs.get('data').get('pin_code')), key).decode("utf-8")
        if 'pin_code_key_id' in inputs.get('data'):
            inputs['data']['pin_code_key_id'] = key_id
        if 'key_id' in inputs.get('data') and inputs['data']['key_id'] is None:
            inputs['data']['key_id'] = key_id
    if 'params' in inputs and 'pin_code' in inputs['params']:
        key_id, key = get_encryption(env, inputs['params']['app_id'])
        inputs['params']['pin_code'] = rsa(sha3256(inputs.get('params').get('pin_code')), key).decode("utf-8")
        if 'pin_code_key_id' in inputs.get('params'):
            inputs['params']['pin_code_key_id'] = key_id
        if 'key_id' in inputs.get('params') and inputs['data']['key_id'] is None:
            inputs['params']['key_id'] = key_id


def encode_password(env, inputs):
    if inputs.get('data', False) and 'password_e' in inputs['data']:
        if 'encryption' in inputs and inputs['encryption']['type'] == '3DES':
            inputs['data']['password_e'] = des3_encrypt(inputs['data']['password_e'], inputs['encryption']['key'])
            del (inputs['encryption'])
        else:
            key_id, key = get_encryption(env, inputs['params']['app_id'])
            inputs['data']['password_e'] = rsa(sha3256(inputs.get('data').get('password_e')), key).decode("utf-8")
            inputs['data']['key_id'] = key_id
    if 'params' in inputs and 'password_e' in inputs['params']:
        key_id, key = get_encryption(env, inputs['params']['app_id'])
        inputs['params']['password_e'] = rsa(sha3256(inputs.get('params').get('password_e')), key).decode("utf-8")
        inputs['params']['key_id'] = key_id


# multipart/form-data
# @staticmethod
def format(inputs):
    """
    form data
    :param: data:  {"req":{"cno":"18990876","flag":"Y"},"ts":1,"sig":1,"v": 2.0}
    :param: boundary: "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    :param: headers: 包含boundary的头信息；如果boundary与headers同时存在以headers为准
    :return: str
    :rtype: str
    """
    data = inputs.get('data', '')
    headers = inputs.get('headers', '')
    # boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"


    # 从headers中提取boundary信息
    if "Content-Type" in headers:
        fd_val = str(headers["Content-Type"])
        if "boundary" in fd_val:
            fd_val = fd_val.split(";")[1].strip()
            boundary = fd_val.split("=")[1].strip()
        else:
            logging.error("multipart/form-data头信息错误，请检查content-type key是否包含boundary")
    # form-data格式定式
    jion_str = '--{}\r\nContent-Disposition: form-data; name="{}"\r\n\r\n{}\r\n'
    end_str = "--{}--".format(boundary)
    args_str = ""

    if not isinstance(data, dict):
        logging.error("multipart/form-data参数错误，data参数应为dict类型")
    for key, value in data.items():
        args_str = args_str + jion_str.format(boundary, key, value)

    args_str = args_str + end_str.format(boundary)
    args_str = args_str.replace("\'", "\"")
    inputs["data"] = args_str
    return inputs