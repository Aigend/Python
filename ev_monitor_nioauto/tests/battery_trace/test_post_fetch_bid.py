# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/04
@api: POST_/api/1/in/battery/fetch_bid
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=31266
@description: 通过GBT国标编码查询电池的bid（VMS生成的内部电池包id），如果没查到，则为该电池包生成一个bid绑定。和get_bid 不同的地方在于，这个接口会带上 nio_encoding，如果没查到，不光生成bid，连nio编码也一起写入
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.random_tool import generate_battery_pack, generate_random_gbt_code, generate_random_nio_code
from utils.assertions import assert_equal

app_id = 100078
create_battery_path = '/api/1/in/battery/receiveBatteryProduce'
fetch_bid_path = '/api/1/in/battery/fetch_bid'


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
    # 生成一个不存在的电池包编码，用于验证生成bid并保存记录
    non_exist_gbt_code = generate_random_gbt_code('03U', 'P')
    _, non_exist_nio_encoding = generate_random_nio_code()
    # 确保该code不存在在db中
    mysql['battery_trace'].delete('sys_battery_pack_entity', {'code': non_exist_gbt_code})
    result['non_exist_gbt_code'] = non_exist_gbt_code
    result['non_exist_nio_encoding'] = non_exist_nio_encoding
    yield result
    with allure.step('测试完成后删除创建的电池数据'):
        mysql['battery_trace'].delete('sys_battery_pack_entity', {'code': result['gbt_code']})
        mysql['battery_trace'].delete('sys_battery_module_entity', {'pack_id': result['gbt_code']})
        mysql['battery_trace'].delete('sys_battery_pack_entity', {'code': non_exist_gbt_code})


def test_post_get_fetch_bid(env, mysql, create_battery_pack):
    with allure.step('查询电池包的bid'):
        http = {
            "host": env['host']['tsp_in'],
            "path": fetch_bid_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": {'list': [{'code': create_battery_pack['gbt_code']}]}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
        assert response['data'][create_battery_pack['gbt_code']]
    with allure.step('查询不存在的电池包，生成bid并写入nio编码'):
        http = {
            "host": env['host']['tsp_in'],
            "path": fetch_bid_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": {'list': [{'code': create_battery_pack['non_exist_gbt_code'],
                               'nio_encoding': create_battery_pack['non_exist_nio_encoding']}]}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
        assert response['data'][create_battery_pack['non_exist_gbt_code']]
    with allure.step('检查数据库中生成了不存在的电池包的数据，同时生成bid并写入nio编码'):
        record = mysql['battery_trace'].fetch_one('sys_battery_pack_entity',
                                                  {'code': create_battery_pack['non_exist_gbt_code']})
        assert record and record['bid'] and record['nio_encoding']
