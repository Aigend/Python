#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/13 12:01
@contact: li.liu2@nio.com
@description:
    获取openvpn的server节点信息
    http://showdoc.nevint.com/index.php?s=/13&page_id=25077

"""
import json
import allure
import pytest

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


@pytest.mark.skip("deprecated")
class TestMeesageAPI(object):
    def test_vpn_endpoints(self, env):
        """
        获取openvpn的server节点信息
        http://showdoc.nevint.com/index.php?s=/13&page_id=25077

        """
        inputs = {
            "host": env['host']['tsp_in'],
            "path": "/api/1/message/vpn/endpoints",
            "method": "GET",
            "headers": {'Content-Type': 'application/x-www-form-urlencoded'},
            'params': {'app_id': '10005', 'hash_type': 'sha256', 'sign': ''}
        }
        expect = {
            "data": [
                {
                    "port": 1194,
                    "min_ver": "2.4.9",
                    "status": "Recommended",
                    "region": "CN",
                    "max_user_count": 250,
                    "longitude": 127.191,
                    "latitude": 31.281,
                    "ipaddress": "218.97.15.202",
                    "inner_ipaddress": "10.10.129.254"
                },
                {
                    "port": 1195,
                    "min_ver": "2.4.9",
                    "status": "Recommended",
                    "region": "CN",
                    "max_user_count": 250,
                    "longitude": 116.403,
                    "latitude": 39.923,
                    "ipaddress": "218.97.15.202",
                    "inner_ipaddress": "10.10.128.116"
                }
            ],
            "result_code": "success",
        }
        response = hreq.request(env, inputs)

        check_response(response, expect)


def check_response(response, expect):
    with allure.step('校验response'):
        response.pop('request_id', '')
        response.pop('server_time', '')
        for data in response['data']:
            data.pop('online_user_count')
        response.pop('server_time', '')
        assert_equal(response, expect)
