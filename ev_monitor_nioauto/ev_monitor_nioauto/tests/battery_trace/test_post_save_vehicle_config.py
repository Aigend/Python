# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/17
@api: POST_/api/1/in/battery/save_vehicle_config
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=31697
@description: 车辆配置号
"""

import pytest
import allure
import random
import string
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal


# 为了避免脏数据过多，作为主键的vehicle_config_id保持一致不使用随机值
# vehicle_config_id我们只负责保存值，不做校验，但原则上遵从model_id加_1,_2...后缀这种形式
@pytest.mark.parametrize('upload_now, vehicle_config_id, model_id, factory_id, pack_model_id, expectation, check_db',
                         [
                             (False, 'HFC6502ECSEV6-W-1', 'HFC6502ECSEV6-W',
                              ''.join(random.choices(string.digits + string.ascii_uppercase, k=18)),
                              ''.join(random.choices(string.digits + string.ascii_uppercase, k=10)),
                              'success', True),
                             # 因为暂时没有上传国家平台接口的访问权限，所以这里暂时报internal_error错误
                             (True, 'HFC6502ECSEV6-W-1', 'HFC6502ECSEV6-W',
                              ''.join(random.choices(string.digits + string.ascii_uppercase, k=18)),
                              ''.join(random.choices(string.digits + string.ascii_uppercase, k=10)),
                              'internal_error', False),
                             (False, '', 'temp', 'temp', 'temp', 'invalid_param', False),
                             (False, 'temp', '', 'temp', 'temp', 'invalid_param', False),
                             (False, 'temp', 'temp', '', 'temp', 'invalid_param', False),
                             (False, 'temp', 'temp', 'temp', '', 'invalid_param', False),
                         ],
                         ids=['车辆配置号信息不上报国家平台',
                              '车辆配置号信息上报国家平台',
                              '未提供vehicle_config_id',
                              '未提供model_id',
                              '未提供factory_id',
                              '未提供pack_model_id',
                              ])
def test_post_save_vehicle_config(env, mysql, upload_now, vehicle_config_id, model_id, factory_id, pack_model_id,
                                  expectation, check_db):
    app_id = 100078
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
                'upload_now': upload_now, 'vehicle_config_id': vehicle_config_id, 'model_id': model_id,
                'factory_id': factory_id, 'pack_model_id': pack_model_id
            }
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], expectation)
    if check_db:
        with allure.step('校验db中的值是否正确'):
            record = mysql['battery_trace'].fetch_one('vehicle_config', {'vehicle_config_id': vehicle_config_id})
            assert_equal(record['model_id'], model_id)
            assert_equal(record['factory_id'], factory_id)
            assert_equal(record['pack_model_id'], pack_model_id)
            assert_equal(record['status'], -2)
