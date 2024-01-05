# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/05
@api: GET_/api/1/in/battery/statistics
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=23855
@description: 统计数据
"""

import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal


def test_get_change_vehicle_status(env):
    app_id = 100078
    with allure.step(f'取得统计数据'):
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/statistics',
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
        assert response['data']
