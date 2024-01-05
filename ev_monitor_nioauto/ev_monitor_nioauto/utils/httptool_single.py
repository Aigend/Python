#!/usr/bin/env python
# coding=utf-8

"""
@author: yongqing.wu
@contact: yonqing.wu@nio.com
@version: 1.0
@file: httptool.py
@time: 2017/10/9 下午11:16
"""
import json
import copy
import allure
import requests as r
import codecs
import hashlib
import time
from urllib.parse import urlparse

import logging

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

def string_to_dict(str):
    try:
        str = str.strip().strip('&').split("&")
        return dict([iterm.split("=") for iterm in str])
    except Exception:
        return {}

app_sec = {
    '10000': 'acbd18db4cc2f85cedef654fccc4a4d8',
    '10001': 'e5b57f8542b96193e4b0dfe8a96b6cc0',
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
    '30010':'1b3424e49a4b402c9fb8a6d2dc662cb8'
}


class Sign(object):
    def md5_sig(self, r=None):
        param = {}
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
        print('Sign string is:\n{0}'.format(sig_param))
        sig = hashlib.md5(sig_param.encode('utf-8')).hexdigest()
        query_param.update(timestamp=str(param['timestamp']), sign=sig)

def show_json(json_obj):
    obj = copy.deepcopy(json_obj)
    _convert_obj(obj)

    json_dump_str = json.dumps(obj, indent=2, ensure_ascii=False)
    return json_dump_str


def _convert_obj(obj):
    # Convert obj to make it can be json dumped. Now we just handle the bytes value
    if isinstance(obj, dict):

        for k,v in obj.items():
            if isinstance(v, bytes):
                obj[k]= codecs.encode(obj[k], 'hex').decode('ascii').upper()
            _convert_obj(v)

    elif isinstance(obj, list):
        for item in obj:
            _convert_obj(item)

    else:
        return obj


def request(method, url, **kwargs):
    with MyRequest() as session:
        return session.request(method, url, **kwargs)


class MyRequest(r.Session):
    def __init__(self):
        super(MyRequest, self).__init__()

        self.auth = None
        self.headers = {}
        self.data = {}
        self.params = {}
        self.url = None
        self.is_log = True
        self.response = None
        self.method = None
        self.pre_request = None
        self.curl = None

    @staticmethod
    def _url_param_to_dict(string):
        try:
            string = string.strip().strip('&').split("&")
            return dict([iterm.split("=") for iterm in string])
        except Exception as E:
            return {}

    @staticmethod
    def _dict_to_url_param(diction):
        param_str = ''
        for k, v in diction.items():
            param_str += '&' + str(k) + '=' + str(v)
        return param_str[1:]

    def set_headers(self):
        pass

    def add_headers(self, header):
        self.headers.update(header)

    def set_token(self):
        pass

    def requset_param_logs(self):
        print('request is :\n{0}'.format(self.curl))
        print('header is :{0}'.format(self.headers))
        print('uri params is:{0}'.format(show_json(self.params)))
        if isinstance(self.data, str):
            data = json.loads(self.data)
            print('payload is:\n{0}'.format(show_json(data)))
        else:
            print('payload is:\n{0}'.format(show_json(self.data)))

    def get_curl_request(self):

        urls = self.url
        if self.params:
            urls += "?" + self._dict_to_url_param(self.params)
        curl_str = "curl -X {method} \'{url}\'".format(method=self.method.upper(), url=urls)
        if self.headers:
            for k, v in self.headers.items():
                curl_str += " -H \'{key}:{value}\'".format(key=k, value=v)
        if self.data:
            if isinstance(self.data, dict):
                curl_str = curl_str + " -d \'{data_str}\'".format(data_str=self._dict_to_url_param(self.data))
            elif isinstance(self.data, str):
                curl_str = curl_str + " -d \'{data_str}\'".format(data_str=self.data)
        if self.cert:
            curl_str = curl_str + " --tlsv1.2 --cert {cert} --key {key}".format(cert=self.cert[0],
                                                                                key=self.cert[1])
            if self.verify:
                curl_str = curl_str + " --cacert {cacert}".format(cacert=self.verify)
            else:
                curl_str = curl_str + " -k"
        self.curl = curl_str
        allure.attach("{0}".format(self.curl),"curl请求")

    # def set_sign(self, auth=Md5Sig):
    #     self.is_sign = None
    #     auth(self)
    def clear_param(self):
        self.params = {}
        self.data = {}
        self.headers = {}
        self.url = ''

    def request(self, method, url,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                auth=None,
                timeout=None,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                is_sign=True,
                **kwargs):
        if params:
            self.params = copy.deepcopy(params)
        if headers:
            self.headers = copy.deepcopy(headers)
        if url:
            self.url = url
        if data:
            if headers and headers.get('content-type') == 'application/json':
                self.data = json.dumps(copy.deepcopy(data))
            else:
                self.data = copy.deepcopy(data)

        if kwargs.get('cert'):
            self.cert=kwargs['cert']
        if kwargs.get('verify'):
            self.verify=kwargs['verify']

        self.method = method

        if is_sign:
            self.sign = Sign()
            self.sign.md5_sig(self)

        self.get_curl_request()
        if self.is_log:
            self.requset_param_logs()
        self.response = r.request(self.method, self.url, params=self.params, auth=self.auth,
                                  data=self.data, headers=self.headers if self.headers else None,
                                  **kwargs)

        try:
            re = show_json(self.response.json())
        except ValueError:
            re = self.response.text
        allure.attach("{0}".format(re),"response响应")
        print('Response  is [{0}]:\n{1}'.format(self.response.status_code, re))
        self.clear_param()
        assert self.response.status_code == 200
        return self.response


if __name__ == "__main__":
    # test
    vid = '77c817f946014690b126a6d70be0f858'
    vid = '4e18c0f0ab734805a802b845a02ad824'
    account_id = 212409581
    api = '/api/1/data/report'

    event = json.dumps([{"longitude": "121.230858",
                         "app_ver": "1.0.82.01",
                         "city": "上海市",
                         "area_code": "310104",
                         "app_id": "30009",
                         "nation": "中国",
                         "district": "闵行区",
                         "event_type": "nav_period",
                         "latitude": "31.316501",
                         "timestamp": int(time.time() * 1000),
                         "province": "上海市",
                         "roadName": "合川路"}])
    data = {
        'model': 'ES8',
        'os': 'android',
        'os_ver': '1.0.0',
        'os_lang': 'unknown',
        'os_timezone': 'unknown',
        'client_timestamp': str(int(time.time() - 8 * 3600)),
        'network': 'unknwon',
        'user_id': account_id,
        'vid': vid,
        'events': event

    }

    res = request('POST', url='https://tsp-test.nio.com' + api, data=data)
    print(res.json())