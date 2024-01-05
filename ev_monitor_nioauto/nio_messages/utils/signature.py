#!/usr/bin/env python
# coding=utf-8
import hashlib
import time
from urllib.parse import urlparse

from .commonlib import string_to_dict
import logging

app_sec = {
    '10001': 'e5b57f8542b96193e4b0dfe8a96b6cc0',
    '10005': 'b207319e51865e85e01c15cb29804b55',
    '10016': 'cbaa22028ddd4b169e4ce452a3138afd',
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
        logging.debug('Sign string is:\n{0}'.format(sig_param))
        sig = hashlib.md5(sig_param.encode('utf-8')).hexdigest()
        query_param.update(timestamp=str(param['timestamp']), sign=sig)
