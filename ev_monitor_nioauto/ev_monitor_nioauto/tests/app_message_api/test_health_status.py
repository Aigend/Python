#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    检查Message API DB 状态
    http://showdoc.nevint.com/index.php?s=/13&page_id=12887
"""

import allure
import pytest

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq

@pytest.mark.skip("deprecated")
def test_health_status(env):
    """
    检查Message API DB 状态
    http://showdoc.nevint.com/index.php?s=/13&page_id=12887
    """
    inputs = {
        "host": env['host']['app_in'],
        "path": "/api/1/in/message/health_status",
        "method": "GET"
    }

    response = hreq.request(env, inputs)
    expect = {"result_code": "success"}
    response.pop('request_id', '')
    response.pop('server_time', '')
    assert_equal(response, expect)


def check_response(response, http):
    with allure.step('校验response'):
        response.pop('request_id', '')
        response.pop('server_time', '')
        assert_equal(response, http['expect'])
