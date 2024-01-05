# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/18
@api:  POST_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=31747
@description: 查询车辆配置号列表
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal

app_id = 100078


@pytest.fixture(autouse=True)
def prepare(env):
    # 确保车辆配置号信息有记录
    with allure.step('添加车辆配置号'):
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/save_vehicle_config',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": {
                'upload_now': False, 'vehicle_config_id': 'HFC6502ECSEV6-W-1', 'model_id': 'HFC6502ECSEV6-W',
                'factory_id': 'BNB8DANYEE94ZQZ4JN', 'pack_model_id': 'MBZ00LN15M'
            }
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')


def test_post_graphql_vehicle_config_list(env, mysql):
    graphql = f"""
        {{
            vehicle_configs (page: 1, page_size: 2, vehicle_config_id: "") {{
                page
                page_size
                total
                list {{
                    vehicle_config_id
                    model_id
                    factory_id
                    pack_model_id
                    status
                }}
            }}
        }}
        """
    with allure.step('查询车辆配置号列表'):
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
        assert_equal(response['result_code'], 'success')
        assert len(response['data']['vehicle_configs']['list']) > 0

