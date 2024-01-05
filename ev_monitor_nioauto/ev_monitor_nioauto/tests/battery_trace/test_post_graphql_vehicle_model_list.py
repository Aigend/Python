# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/18
@api:  POST_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=31740
@description: 查询车辆公告号列表
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal

app_id = 100078


@pytest.fixture(autouse=True)
def prepare(env):
    # 确保车辆公告号信息有记录
    with allure.step('添加车辆公告号'):
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/save_vehicle_model',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": {
                'upload_now': False, 'model_id': 'HFC6502ECSEV6-W',
                'batch_number': 666, 'generic_name': 'ES8',
                'vehicle_brand': '蔚来', 'vehicle_name': 'name', 'vehicle_type': 1
            }
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')


def test_post_graphql_vehicle_model_list(env):
    graphql = f"""
        {{
            vehicle_models (page: 1, page_size: 2, model_id: "", batch_number: "", generic_name: "") {{
                page
                page_size
                total
                list {{
                    model_id
                    batch_number
                    generic_name
                    status
                    vehicle_brand
                    vehicle_name
                    vehicle_type
                }}
            }}
        }}
        """
    with allure.step('查询车辆公告号列表'):
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
        assert len(response['data']['vehicle_models']['list']) > 0
