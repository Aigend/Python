#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    get jvm dns cache info
    http://showdoc.nevint.com/index.php?s=/13&page_id=12914
"""

import allure

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


def test_dns_cache(env):
    """
    get jvm dns cache info
    http://showdoc.nevint.com/index.php?s=/13&page_id=12914
    """
    inputs = {
        "host": env['host']['app_in'],
        "path": "/api/1/in/message/dns_cache",
        "method": "GET",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "params": {
            "hash_type": "md5",
            "app_id": "10006",
            'hostname': 'tsp-test-int.nio.com',
            'sign': ''
        }
    }

    response = hreq.request(env, inputs)
    with allure.step('校验response'):
        response.pop('request_id', '')
        response.pop('server_time', '')
        response['data'].pop('ip')
        expect = {'data': {'hostname': 'tsp-test-int.nio.com', 'networkaddress.cache.ttl': '10'}, 'result_code': 'success'}
        assert_equal(response, expect)
