# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/17
@api: POST_/api/1/in/battery/save_vehicle_model
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=31669
@description: 车辆公告号
"""

import pytest
import allure
import random
from random import randint
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal


# 为了避免脏数据过多，作为主键的model_id保持一致不使用随机值
@pytest.mark.parametrize(
    'upload_now, model_id, batch_number, generic_name, vehicle_name, vehicle_type, vehicle_brand, expectation, check_db',
    [
        (False, 'HFC6502ECSEV6-W', randint(100, 999), 'ES8', 'name', random.choice([1, 2, 3, 4]), 'brand', 'success',
         True),
        # 因为暂时没有上传国家平台接口的访问权限，所以这里暂时报internal_error错误
        (True, 'HFC6502ECSEV6-W', randint(100, 999), 'ES8', 'name', 1, 'brand', 'internal_error', False),
        (False, '', 666, 'ES8', 'name', 1, 'brand', 'invalid_param', False),
        (False, 'temp', None, 'ES8', 'name', 1, 'brand', 'invalid_param', False),
        (False, 'temp', 777, '', 'name', 1, 'brand', 'invalid_param', False),
        (False, 'temp', 777, 'ES8', None, 1, 'brand', 'invalid_param', False),
        (False, 'temp', 777, 'ES8', 'name', None, 'brand', 'invalid_param', False),
        (False, 'temp', 777, 'ES8', 'name', 1, '', 'invalid_param', False),
    ],
    ids=[
        '车辆公告号信息不上报国家平台',
        '车辆公告号信息上报国家平台',
        '未提供model_id',
        '未提供batch_number',
        '未提供generic_name',
        '未提供vehicle_name',
        '未提供vehicle_type',
        '未提供vehicle_brand',
    ])
def test_post_save_vehicle_model(env, mysql, upload_now, model_id, batch_number, generic_name, vehicle_name,
                                 vehicle_type, vehicle_brand, expectation, check_db):
    app_id = 100078
    with allure.step('添加车辆公告号'):
        json = {
            'upload_now': upload_now, 'model_id': model_id, 'batch_number': batch_number, 'generic_name': generic_name,
            'vehicle_name': vehicle_name, 'vehicle_type': vehicle_type, 'vehicle_brand': vehicle_brand
        }
        json = {k: v for k, v in json.items() if v is not None}
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/save_vehicle_model',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": json
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], expectation)
    if check_db:
        with allure.step('校验db中的值是否正确'):
            record = mysql['battery_trace'].fetch_one('vehicle_model', {'model_id': model_id})
            assert_equal(record['batch_number'], batch_number)
            assert_equal(record['generic_name'], generic_name)
            assert_equal(record['status'], -2)
