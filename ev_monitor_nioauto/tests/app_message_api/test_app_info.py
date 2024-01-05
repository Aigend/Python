#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    统计App ID 所对应不同app_version的clients数目
    http://showdoc.nevint.com/index.php?s=/13&page_id=365

"""
import allure
import pytest

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


@pytest.mark.skip("deprecated")
def test_app_info(env, cmdopt):
    inputs = {
        "host": env['host']['app_in'],
        "path": "/api/1/in/message/app_info",
        "method": "GET",
        "headers": {
        },
        "params": {
            "hash_type": "sha256",
            'app_id': '10000',
            "app_ids": 1000003 if 'marcopolo' in cmdopt else 10001
        },
    }
    with allure.step("app info api"):
        response = hreq.request(env, inputs)
        assert response.get("result_code") == "success"
        data_len = len(response.get('data', []))
        assert_equal(data_len > 0, True)
