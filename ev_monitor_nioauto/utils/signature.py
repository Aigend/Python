#!/usr/bin/env python
# coding=utf-8
import base64
import hashlib
import time
import json
import logging
import requests
from urllib.parse import urlparse

from utils.commonlib import string_to_dict
from utils.logger import logger
import unpaddedbase64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as PKCS
from Crypto.Hash import SHA3_256
from Crypto.Hash import SHA256
from Crypto.Signature.pss import MGF1

consts = [
    "2976ae25f6b04f719f351e2fd890fa50",
    "ed8abe8d1fc3456a8a1e366151c2a6b7",
    "6b10b3f89d1c4bfa8199ff3f74aa2887",
    "a76d51834a4f4609a38d1a0f5e3d6465",
    "e6be849e07c64511a17b777743021af3",
    "3edb5e23e8b34f848af4888feb169e9b",
    "c527b8e5816346c6a586e7ea9db27fa5",
    "bb719cd4f60d4567a19103187e855b30",
    "85c9ff17d6cf46bbbea8e8671d25a944",
    "9341dc8b84bb422598a890273a28fe09"
]

app_sec = {
    '10000': 'acbd18db4cc2f85cedef654fccc4a4d8',
    '10001': '4AE54A0CF4C8B3E4f3E0d24C34A42068',  # stg
    # '10001': '89b7897F8EeC62e3C96892581aB2A422',  # test
    '10002': '2bc9b00fdcf8f7ded6d77afdd7077e79',
    '10003': 'f174b769ad18af17c0f65b83214ac0cc',
    '10004': '7936e30cb1b8948ac2f283871642029c',
    '10005': 'b207319e51865e85e01c15cb29804b55',
    '10006': '68f828215165cd42cab37e8643a00019',
    '10016': 'cbaa22028ddd4b169e4ce452a3138afd',
    '10023': '18aca711d33d5c318a9ade7b22a3d341',
    '30006': '93ee15dab422478289d4def041193134',
    '10066': '0ca7836511d143279a0ec04773c4b19b',
    '80001': 'ce058c35eed7458180eaf877d35fda83',
    '30007': '3ca9b9c97ae94f2dacabc006d8eaad1c',
    '30015': '2cc06d48db80431f99171404f593883c',
    '10014': '6396c6d430dd48809fea88fb01d94cce',
    '10022': '2f1f42e22ea484b2f9db2049540066c0',
    '10013': '33a130f9425063421cd9e7b6ed6050a5',
    '100008': 'bD6f916F622aBecF77d638E485A1B2f4',
    '100006': '6295f98351F04a0e575aC8e8fD6e1Bde',
    '100078': 'd430BD27cbE77FcEf186f2158184F80b',
    '10008': '4cfdb3115a617a508ef584f896c08133',
    '10107': '8d8c1c8295a6458c83e40a62c7a0970f',
    '10666': '0ee61e5591dd4c94ae7031daadc028cc',
    '30010': '1b3424e49a4b402c9fb8a6d2dc662cb8',
    '10007': 'ae108a49688ab8b87f392b452d43829e',
    '100395': 'abDc40A5097f6719Fe6bC947c6087c16',
    '100058': '48947b41b9c2e945cDb763cdAE1b9ba6',
}

app_sec_env = {
    'test': {
        '10007': 'ae108a49688ab8b87f392b452d43829e',
        '10022': '2f1f42e22ea484b2f9db2049540066c0',
    },
    'stg': {}
}


def encrypt(password, key):
    keyDER = unpaddedbase64.decode_base64(key)
    keyPub = RSA.importKey(keyDER)
    cipher = PKCS.new(keyPub, SHA3_256, lambda x, y: MGF1(x, y, SHA256))
    cipher_text = cipher.encrypt(password.encode())
    return base64.urlsafe_b64encode(cipher_text)


def checkedPassword(password, key):
    salt = consts[ord(password[0]) % len(consts)]
    sh = SHA3_256.new()
    sh.update((password + salt).encode("utf-8"))
    ps = sh.hexdigest()
    return encrypt(ps, key)


class Sign(object):
    def md5_sig(self, r=None):
        param = {}
        # sign_type = 'sha256'
        body_param = getattr(r, "data", {})
        query_param = getattr(r, 'params', {})
        headers = getattr(r, 'headers', {})
        if body_param:
            if headers.get('content-type') == 'application/json':
                param.update(jsonBody=body_param)
            elif isinstance(body_param, str):
                param.update(string_to_dict(body_param))
            else:
                param.update(body_param)
        param.update(query_param)
        try:
            common_keys = set(query_param.keys()) & set(body_param.keys())
            for k in common_keys:
                param[k] = [query_param[k], body_param[k]]
                print(k, param[k])
        except Exception as e:
            pass

        param['timestamp'] = int(time.time())
        # if 'hash_type' in param.keys():
        #     sign_type = param['hash_type']
        # else:
        #     param['hash_type'] = sign_type
        keys = sorted(param.keys())
        param_str = ''
        token = ''
        for key in keys:
            value = param[key]
            if str(value) and value != '':
                if isinstance(value, list):
                    value.sort()
                    for v in value:
                        param_str += str(key) + '=' + str(v) + '&'
                else:
                    param_str += str(key) + '=' + str(value) + '&'
            else:
                param_str += str(key) + '=&'
        app_id = str(query_param.get('app_id'))
        app_secret = app_sec.get(app_id, 'unknow_app_id_{0}'.format(app_id))
        sig_param = r.method + urlparse(r.url).path + "?" + param_str[:-1] + app_secret
        for head_key in r.headers:
            if head_key.lower() == "authorization":
                token = r.headers[head_key]
        sig_param += token
        logger.debug('Sign string is:\n{0}'.format(sig_param))
        # sig = hashlib.md5(sig_param.encode('utf-8')).hexdigest()
        if 'hash_type' in param.keys() and param['hash_type'] == 'sha256':
            sig = hashlib.sha256(sig_param.encode('utf-8')).hexdigest()
        else:
            sig = hashlib.md5(sig_param.encode('utf-8')).hexdigest()
        query_param.update(timestamp=str(param['timestamp']), sign=sig)


def moatkeeper_signature_old(method, path, url_params, data_body, json_body, secret, token):
    """
    签名字符串格式：
    ${httpMethod}+${PATH}+'?'+'${key}=${value}&${key}=${value}&${key}=${value}'+${appSecret}+${access_token}
    :param method: 请求方法
    :param path: 请求路径
    :param url_params: 请求参数
    :param data_body: 请求体参数，Content-Type为application/x-www-form-urlencoded时传
    :param json_body: 请求体参数，Content-Type为application/json时传
    :param secret: 与app_id对应的密码
    :param token: Authorization的值
    :return: 签名sign字符串
    """
    sign = ""
    sign += method
    sign += path
    sign += "?"
    sign_type = 'md5'

    # 组合param、data和json
    all_parameters = {}
    url_params_keys = []
    data_body_keys = []
    if url_params:
        if 'hash_type' in url_params.keys():
            sign_type = url_params['hash_type']
        url_params.update({'timestamp': int(time.time())})
        all_parameters.update(url_params)
        url_params_keys = url_params.keys()
    if data_body:
        all_parameters.update(data_body)
        data_body_keys = data_body.keys()
    if json_body:
        all_parameters.update(jsonBody=json.dumps(json_body))

    # url参数和body参数有相同key时，将value作为列表存下来
    common_keys = set(url_params_keys) & set(data_body_keys)
    for k in common_keys:
        all_parameters[k] = sorted([url_params[k], data_body[k]])

    if all_parameters:
        # 排序
        sorted_all_parameters = dict(sorted(all_parameters.items(), key=lambda x: x[0]))
        kv = []
        for key, value in sorted_all_parameters.items():
            if key != 'sign':
                if not isinstance(value, list):
                    kv.append("=".join([str(key), str(value)]))
                else:
                    same_key = []
                    # 排序
                    for v in sorted(value):
                        same_key.append("=".join([str(key), str(v)]))
                    kv.append("&".join(same_key))
        sign += "&".join(kv)

    sign += secret
    if token:
        sign += token
    logging.info("签名字符串：" + sign)
    if sign_type == 'sha256':
        return hashlib.sha256(sign.encode('utf-8')).hexdigest()
    else:
        return hashlib.md5(sign.encode('utf-8')).hexdigest()


def moatkeeper_signature(inputs, secret, token=None):
    """
    签名字符串格式：
    ${httpMethod}+${PATH}+'?'+'${key}=${value}&${key}=${value}&${key}=${value}'+${appSecret}+${access_token}
    :param inputs: {
                    "method": 请求方法,
                    "path": 请求路径,
                    "headers": 请求头,
                    "params": 请求参数,
                    "data": 请求体参数，Content-Type为application/x-www-form-urlencoded时传,
                    "json": 请求体参数，Content-Type为application/json时传
                    "files": 上传文件时
                    }
    :param secret: 与app_id对应的密码
    :param token: Authorization的值
    :return: 签名sign字符串
    """

    sign = ""
    sign += inputs.get("method")
    sign += inputs.get("path")
    sign += "?"
    sign_type = "md5"

    # 组合param、data和json
    all_parameters = {}
    url_params_keys = []
    data_body_keys = []
    url_params = inputs.get("params")
    data_body = inputs.get("data")
    json_body = inputs.get("json")
    files = inputs.get("files")
    if url_params:
        sign_type = url_params.get("hash_type") if url_params.get("hash_type") else sign_type
        url_params.update({'timestamp': int(time.time())})
        all_parameters.update(url_params)
        url_params_keys = url_params.keys()
    # 不传content-type时，默认为application/x-www-form-urlencoded，data参与签名计算
    content_type = inputs.get('headers', {}).get("content-type", "application/x-www-form-urlencoded")
    if "application/x-www-form-urlencoded" in content_type and data_body and not files:
        # content_type 类型为application/x-www-form-urlencoded对data进行签名计算，传files时data数据不参与签名计算
        all_parameters.update(data_body)
        data_body_keys = data_body.keys()
    if "application/json" in content_type and json_body:
        all_parameters.update(jsonBody=json.dumps(json_body))

    # url参数和body参数有相同key时，将value作为列表存下来
    common_keys = set(url_params_keys) & set(data_body_keys)
    for k in common_keys:
        all_parameters[k] = sorted([url_params[k], data_body[k]])

    if all_parameters:
        # 排序
        sorted_all_parameters = dict(sorted(all_parameters.items(), key=lambda x: x[0]))
        kv = []
        for key, value in sorted_all_parameters.items():
            if key != 'sign':
                if not isinstance(value, list):
                    kv.append("=".join([str(key), str(value)]))
                else:
                    same_key = []
                    # 排序
                    for v in sorted(value):
                        same_key.append("=".join([str(key), str(v)]))
                    kv.append("&".join(same_key))
        sign += "&".join(kv)

    sign += secret
    if token:
        sign += token
    logging.info("签名字符串：" + sign)
    if sign_type == 'sha256':
        return hashlib.sha256(sign.encode('utf-8')).hexdigest()
    else:
        return hashlib.md5(sign.encode('utf-8')).hexdigest()


def get_app_secret(env, target_app_id):
    inputs = {"host": env['host']['app_in'],
              "path": "/acc/2/in/app/info_old",
              "method": "GET",
              "params": {
                  "region": "cn",
                  "lang": "zh-cn",
                  "hash_type": "sha256",
                  "app_id": "10007",
                  "target_app_id": target_app_id,
                  "sign": "",
                  "nonce": str(int(time.time() * 1000))
              }
              }
    s = "ae108a49688ab8b87f392b452d43829e"
    inputs['params']["sign"] = moatkeeper_signature(inputs, s, None)
    res = requests.request(inputs["method"], inputs["host"] + inputs["path"], params=inputs["params"])
    response = res.json()
    return response['data']['secret']
