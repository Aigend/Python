# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/04
@api: POST_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=29688
@description: 查询导出记录详情
"""

import allure
import pytest
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal


@pytest.fixture(autouse=True)
def get_data_export_count(env, mysql):
    result = mysql['battery_trace'].fetch_by_sql('select count(1) as count from data_export')
    return result[0]['count']


def test_post_graphql_export_detail(env, get_data_export_count):
    app_id = 100078
    graphql = f"""
    {{
        data_export (id: 1) {{
            id
            key
            url
            action
            status
            expire_at
            message
        }}
    }}
    """
    with allure.step('查询id为1的导出记录'):
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/graphql',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ""
            },
            "json": {'query': graphql}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        if get_data_export_count > 0:
            assert_equal(response['result_code'], 'success')
        else:
            assert_equal(response['debug_msg'], 'record not found')
