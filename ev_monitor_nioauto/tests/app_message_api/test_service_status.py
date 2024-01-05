#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    检查message api所依赖的别的服务的服务状态
    http://showdoc.nevint.com/index.php?s=/13&page_id=12888


"""

import allure
import pytest

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


@pytest.mark.skip("deprecated")
def test_service_status(env):
    """
    检查message api所依赖的别的服务的服务状态
    http://showdoc.nevint.com/index.php?s=/13&page_id=12888
    """
    inputs = {
        "host": env["host"]["app_in"],
        "path": "/api/1/in/message/service_status",
        "method": "GET",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "params": {
            "app_id": "10000",
            "hash_type": "md5",
            "sign": "",
        }
    }

    response = hreq.request(env, inputs)
    with allure.step('校验response'):
        expect = {
            'data': {'account': 'success'},
            'result_code': 'success'
        }
        response.pop('request_id', '')
        response.pop('server_time', '')
        assert_equal(response, expect)
