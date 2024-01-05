# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/18
@api:  POST_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=20011
@description: 查询供应商列表
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal

app_id = 100078


@pytest.fixture(autouse=True)
def prepare(env):
    # 确保供应商信息有记录
    with allure.step('添加供应商'):
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/save_supplier',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": {
                'upload_now': False, 'id': '91320481MA1MNYLY9X', 'name': '江苏时代新能源科技有限公司', 'factory_code': '111',
                'phone': '11111111111', 'email': 'noname@temp.com', 'contacts': 'nobody', 'address': 'nowhere'
            }
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')


def test_post_graphql_supplier_list(env):
    graphql = f"""
        {{
            suppliers (id: "", name: "") {{
                list {{
                    id
                    name
                    factory_code
                    contacts
                    phone
                    email
                    address
                }}
            }}
        }}
        """
    with allure.step('查询供应商列表'):
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
        assert len(response['data']['suppliers']['list']) > 0
