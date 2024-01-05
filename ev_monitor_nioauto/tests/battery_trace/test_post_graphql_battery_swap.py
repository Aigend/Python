# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/11/29
@api: GET_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=32445
@description: 查询模组维修列表
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal

app_id = 100078
graphql_path = '/api/1/in/battery/graphql'


@pytest.fixture(autouse=True)
def get_swap_count(env, mysql):
    result = mysql['battery_trace'].fetch_by_sql('select count(1) as count from repair')
    return result[0]['count']


def test_post_graphql_battery_swap(env, get_swap_count):
    with allure.step('使用graphql查询模组维修列表'):
        graphql = f"""
        {{
            repairs (page: 1, page_size: 2, vin: "", code: "", status: 0, export: false) {{
                page
                page_size
                total
                export_id
                list {{
                    vin
                    old_code
                    new_code
                    status
                    id
                    message
                }}
            }}
        }}
        """
        http = {
            "host": env['host']['tsp_in'],
            "path": graphql_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": {'query': graphql}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
        assert_equal(len(response['data']['repairs']['list']), 0 if get_swap_count == 0 else 1 if get_swap_count == 1 else 2)

