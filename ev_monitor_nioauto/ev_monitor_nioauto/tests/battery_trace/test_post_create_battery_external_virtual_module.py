# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/03
@api: POST_/api/1/battery/save_pack
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=27334
@description: 电池生产信息接口，虚拟模组，外部使用
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.random_tool import generate_battery_pack_with_virtual_module
from utils.assertions import assert_equal

"""
    module id为25位时系统判定其为虚拟模组，
    此时module信息不再保存在sys_battery_module_entity表中，而是直接写入cell表
    每个cell一条记录，所以会保存module数 x cell数条记录
    generate_battery_pack_with_virtual_module会生成12组module，每个module下8个cell
"""

battery_save_pack_keys = 'case_name,repetition_model,repetition_same_mode_cell,repetition_diff_mode_cell,result_code'
battery_save_pack_cases = [
    ("正案例_模组不重复", False, False, False, "success"),
    ("反案例_模组重复", True, False, False, "internal_error"),
    ("反案例_相同模组内的cell重复", False, True, False, "internal_error"),
    ("反案例_不同模组内的cell重复", False, False, True, "internal_error"),
    ("反案例_模组cell都重复", True, True, True, "internal_error"),
]
battery_save_pack_ids = [f"{case[0]}" for case in battery_save_pack_cases]


@pytest.mark.parametrize(battery_save_pack_keys, battery_save_pack_cases, ids=battery_save_pack_ids)
def test_post_create_battery(env, mysql, case_name, repetition_model, repetition_same_mode_cell, repetition_diff_mode_cell, result_code):
    battery_pack = generate_battery_pack_with_virtual_module(repetition_model, repetition_same_mode_cell, repetition_diff_mode_cell)
    with allure.step('生成电池模组'):
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
            "json": {'request_msg': battery_pack['battery_data']}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], result_code)
    if "正案例" in case_name:
        with allure.step('校验电池包在db中已经创建'):
            record = mysql['battery_trace'].fetch('sys_battery_pack_entity', {'code': battery_pack['gbt_code']})
            assert_equal(len(record), 1)
            record = mysql['battery_trace'].fetch('cell', {'pack_id': battery_pack['gbt_code']})
            assert_equal(len(record), 96)
        with allure.step('测试完成后删除创建的电池数据'):
            mysql['battery_trace'].delete('sys_battery_pack_entity', {'code': battery_pack['gbt_code']})
            mysql['battery_trace'].delete('sys_battery_module_entity', {'pack_id': battery_pack['gbt_code']})
            mysql['battery_trace'].delete('cell', {'pack_id': battery_pack['gbt_code']})
