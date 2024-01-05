# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/25
@api:  POST_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=31745
@description: 查询电池单体规格列表
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal

app_id = 100078


@pytest.fixture(autouse=True)
def prepare(env):
    # 确保电池单体规格信息有记录
    with allure.step('添加电池单体规格信息'):
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/save_cell_model',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": {
                'upload_now': False, 'model_id': 'S5E891'
            }
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')


def test_post_graphql_cell_model_list(env):
    graphql = f"""
        {{
            cell_models (page: 1, page_size: 2, model_id: "", status: 0) {{
                page
                page_size
                total
                list {{
                    model_id
                    capacity
                    capacity_c3
                    voltage
                    status
                }}
            }}
        }}
        """
    with allure.step('查询电池单体规格列表'):
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
        assert len(response['data']['cell_models']['list']) > 0
