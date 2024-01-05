#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/13 12:01
@contact: li.liu2@nio.com
@description:
    获取openvpn的dns信息
    http://showdoc.nevint.com/index.php?s=/13&page_id=25078

"""
import json
import allure
import pytest

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


@pytest.mark.skip("deprecated")
class TestMeesageAPI(object):
    def test_vpn_dns(self, env):
        """
        获取openvpn的dns信息
        http://showdoc.nevint.com/index.php?s=/13&page_id=25078

        """
        inputs = {
            "host": env['host']['tsp_in'],
            "path": "/api/1/message/vpn/dns",
            "method": "GET",
            "headers": {'Content-Type': 'application/x-www-form-urlencoded'},
            'params': {'app_id': '10005', 'hash_type': 'sha256', 'sign': ''}
        }
        expect = {
            "data": [
                {
                    "ipaddress": "10.112.17.18",
                    "region": "CN",
                    "location": "shbs"
                },
                {
                    "ipaddress": "10.112.17.17",
                    "region": "CN",
                    "location": "shbs"
                },
                {
                    "ipaddress": "10.10.129.253",
                    "region": "DEU",
                    "location": "frankfurt"
                },
                {
                    "ipaddress": "10.10.128.115",
                    "region": "DEU",
                    "location": "frankfurt"
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
        assert_equal(response, expect)
