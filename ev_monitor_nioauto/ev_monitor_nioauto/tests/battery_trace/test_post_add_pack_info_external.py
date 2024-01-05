# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/04
@api: POST_/api/1/battery/add_pack_extern_info
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=27872
@description: 电池生产扩展信息数据采集接口，提供CATL端使用。 catl上报电池扩展信息，存储于TSP电池溯源管理系统，以便后续提供给DD使用
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.random_tool import generate_battery_add_info
from utils.assertions import assert_equal


@pytest.fixture(autouse=True)
def create_battery_add_info(mysql):
    with allure.step('测试开始前生成电池扩展信息数据'):
        result = generate_battery_add_info()
        print(result['p_code'])
    yield result
    with allure.step('测试完成后删除创建的电池扩展信息'):
        mysql['battery_trace'].delete('edi', {'code': result['p_code']})


def test_post_add_pack_info(env, create_battery_add_info):
    with allure.step('生成电池扩展信息'):
        app_id = 100337
        http = {
            "host": env['host']['tsp_ex'],
            "path": "/api/1/battery/add_pack_extern_info",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ""
            },
            "json": {'request_msg': create_battery_add_info['battery_add_info']}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')

