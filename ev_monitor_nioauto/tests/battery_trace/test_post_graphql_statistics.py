# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2022/01/25
@api: POST_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=32914
@description: 查询统计信息（总量）
"""
import allure

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as restClient

"""
使用https://tsp-test.nioint.com/api/1/in/battery/task?task=12可以手动执行statistics的定时任务
"""


def test_post_graphql_statistics(env):
    app_id = 100078
    graphql = f"""
        {{
            statistics {{
                pack_all
                pack_uploaded
                produce_all
                produce_success
                produce_failed
                sale_all
                sale_success
                sale_failed
                swap_all
                swap_success
                swap_failed
            }}
        }}
        """
    with allure.step('查询全量统计信息'):
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
