# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/05
@api: GET_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=29384
@description: 查询单个电池包详情，注意并不返回模组信息
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.random_tool import generate_battery_pack
from utils.assertions import assert_equal

app_id = 100078
create_battery_path = '/api/1/in/battery/receiveBatteryProduce'
graphql_path = '/api/1/in/battery/graphql'


@pytest.fixture(autouse=True)
def create_battery_pack(env, mysql):
    with allure.step('测试开始前生成电池包'):
        result = generate_battery_pack()
        http = {
            "host": env['host']['tsp_in'],
            "path": create_battery_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ""
            },
            "json": {'requestMsg': result['battery_data']}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
    yield result
    with allure.step('测试完成后删除创建的电池数据'):
        mysql['battery_trace'].delete('sys_battery_pack_entity', {'code': result['gbt_code']})
        mysql['battery_trace'].delete('sys_battery_module_entity', {'pack_id': result['gbt_code']})


def test_post_graphql_battery_pack(env, create_battery_pack):
    with allure.step('使用graphql查询电池模组列表'):
        graphql = f"""
        {{
            pack (code: "{create_battery_pack['gbt_code']}", bid:"", export: false) {{
                code
                bid
                nio_encoding
                status
                source
                manufacturing_date
                logistic_des
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
        assert_equal(response['data']['pack']['code'], create_battery_pack['gbt_code'])

