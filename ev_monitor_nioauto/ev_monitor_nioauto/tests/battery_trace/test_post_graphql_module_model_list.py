# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/25
@api:  POST_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=31771
@description: 查询电池模组规格列表
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal

app_id = 100078


@pytest.fixture(autouse=True)
def prepare(env):
    # 确保电池单体规格信息有记录
    with allure.step('添加电池模组规格信息'):
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/save_module_model',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": {
                'upload_now': False, 'model_id': 'BAC0702008'
            }
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')


def test_post_graphql_module_model_list(env):
    graphql = f"""
        {{
            module_models (page: 1, page_size: 2, model_id: "", status: 0) {{
                page
                page_size
                total
                list {{
                    model_id
                    status
                }}
            }}
        }}
        """
    with allure.step('查询电池模组规格列表'):
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
        assert len(response['data']['module_models']['list']) > 0
