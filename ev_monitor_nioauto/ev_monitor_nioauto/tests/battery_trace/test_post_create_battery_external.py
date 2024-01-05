# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/03
@api: POST_/api/1/battery/save_pack
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=27334
@description: 电池生产信息接口，外部使用
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.random_tool import generate_battery_pack
from utils.assertions import assert_equal

"""
    module id为24位时系统判定其为非虚拟模组，
    此时module信息保存在sys_battery_module_entity表中，
    每个module一条记录，每个module下的cell信息以列表形式保存
    generate_battery_pack会生成32组module，每个module下12个cell
"""


@pytest.fixture(autouse=True)
def create_battery_pack(mysql):
    with allure.step('测试开始前生成电池模组数据'):
        result = generate_battery_pack(is_internal=False)
    yield result
    with allure.step('测试完成后删除创建的电池数据'):
        mysql['battery_trace'].delete('sys_battery_pack_entity', {'code': result['gbt_code']})
        mysql['battery_trace'].delete('sys_battery_module_entity', {'pack_id': result['gbt_code']})


def test_post_create_battery(env, create_battery_pack, mysql):
    with allure.step('生成电池模组'):
        # app_id = 100078
        app_id = 100337
        http = {
            "host": env['host']['tsp_ex'],
            "path": "/api/1/battery/save_pack",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ""
            },
            "json": {'request_msg': create_battery_pack['battery_data']}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
    with allure.step('校验电池包在db中已经创建'):
        record = mysql['battery_trace'].fetch('sys_battery_pack_entity', {'code': create_battery_pack['gbt_code']})
        assert_equal(len(record), 1)
        record = mysql['battery_trace'].fetch('sys_battery_module_entity', {'pack_id': create_battery_pack['gbt_code']})
        assert_equal(len(record), 32)
