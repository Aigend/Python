# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/12/21
@api: GET_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=32446
@description: 查询退役列表
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal

app_id = 100078
graphql_path = '/api/1/in/battery/graphql'


@pytest.fixture(autouse=True)
def get_retire_count(env, mysql):
    result = mysql['battery_trace'].fetch_by_sql('select count(1) as count from retire')
    return result[0]['count']


def test_post_graphql_battery_retire(env, get_retire_count):
    with allure.step('使用graphql查询模组维修列表'):
        graphql = f"""
        {{
            retires (page: 1, page_size: 2, code: "", status: 0, export: false) {{
                page
                page_size
                total
                list {{
                    code
                    message
                    retire_time
                    status
                    retire_type
                    battery_type
                    mass
                    recover_unit_code
                    recover_unit_name
                    retire_unit_code
                    retire_unit_name
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
        assert_equal(len(response['data']['retires']['list']), 0 if get_retire_count == 0 else 1 if get_retire_count == 1 else 2)

