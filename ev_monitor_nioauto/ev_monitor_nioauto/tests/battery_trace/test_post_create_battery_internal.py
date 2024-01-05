# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/03
@api: POST_/api/1/in/battery/receiveBatteryProduce
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=30698
@description: 电池生产信息接口，内部使用
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.random_tool import generate_battery_pack
from utils.assertions import assert_equal


@pytest.fixture(autouse=True)
def create_battery_pack(mysql):
    with allure.step('测试开始前生成电池模组数据'):
        result = generate_battery_pack()
    yield result
    with allure.step('测试完成后删除创建的电池数据'):
        mysql['battery_trace'].delete('sys_battery_pack_entity', {'code': result['gbt_code']})
        mysql['battery_trace'].delete('sys_battery_module_entity', {'pack_id': result['gbt_code']})


def test_post_create_battery(env, create_battery_pack):
    with allure.step('生成电池模组'):
        app_id = 100078
        http = {
            "host": env['host']['tsp_in'],
            "path": "/api/1/in/battery/receiveBatteryProduce",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ""
            },
            "json": {'requestMsg': create_battery_pack['battery_data']}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
