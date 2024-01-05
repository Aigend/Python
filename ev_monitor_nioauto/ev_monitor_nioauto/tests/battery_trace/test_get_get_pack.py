# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/04
@api: GET_/api/1/in/battery/get_pack
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=9578
@description: 通过NIO编码或者gbt编码查询电池信息
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.random_tool import generate_battery_pack
from utils.assertions import assert_equal

app_id = 100078
create_battery_path = '/api/1/in/battery/receiveBatteryProduce'
get_pack_path = '/api/1/in/battery/get_pack'


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


def test_get_get_pack(env, create_battery_pack):
    with allure.step('取得电池包数据'):
        http = {
            "host": env['host']['tsp_in'],
            "path": get_pack_path,
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
                "code": create_battery_pack['gbt_code'],
                "query_type": 1
            },
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
        assert_equal(response['data']['status'], -2)  # 新生成的电池状态都为-2 - 未上报国家平台
        assert_equal(response['data']['logistic_des'], create_battery_pack['logistic_des'])
        assert_equal(response['data']['order_no'], create_battery_pack['order_no'])
