# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2022/01/25
@api: POST_/api/1/in/battery/graphql
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=32880
@description: 查询统计信息（按月）
"""
import allure

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as restClient


def test_post_graphql_statistics_monthly(env):
    app_id = 100078
    graphql = f"""
        {{
            statistics_per_mon (page: 1, page_size: 2, export: false) {{
                page
                page_size
                total
                export_id
                list {{
                  id
                  init_success
                  init_success_rate
                  init_failed
                  init_failed_rate
                  init_count
                  corrected_success
                  corrected_success_rate
                  corrected_failed
                  corrected_failed_rate
                  corrected_count
                  statistic_type
                  statistic_time
                }}
            }}
        }}
        """
    with allure.step('查询月度统计信息'):
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
