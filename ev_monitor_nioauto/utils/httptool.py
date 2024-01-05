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

from utils.logger import logger
from utils.commonlib import show_json
from utils.signature import Sign



@allure.step('发送http请求')
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
        logger.debug('request is :\n{0}'.format(self.curl))
        logger.debug('header is :{0}'.format(self.headers))
        logger.debug('uri params is:{0}'.format(show_json(self.params)))
        if isinstance(self.data, str):
            data = json.loads(self.data)
            logger.debug('payload is:\n{0}'.format(show_json(data)))
        else:
            logger.debug('payload is:\n{0}'.format(show_json(self.data)))

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
        logger.debug('Response  is [{0}]:\n{1}'.format(self.response.status_code, re))
        self.clear_param()
        assert self.response.status_code == 200
        return self.response
