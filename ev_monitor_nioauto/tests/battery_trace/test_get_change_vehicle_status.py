# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/05
@api: GET_/api/1/in/battery/change_vehicle_status
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=23436
@description: 修改车辆状态
"""
import random

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.random_tool import generate_battery_pack
from utils.assertions import assert_equal

app_id = 100078
create_battery_path = '/api/1/in/battery/receiveBatteryProduce'
change_vehicle_status_path = '/api/1/in/battery/change_vehicle_status'


@pytest.fixture(autouse=True)
def create_battery_pack(env, mysql):
    vin = env['vehicles']['colin']['vin']
    vid = env['vehicles']['colin']['vehicle_id']
    with allure.step('测试开始前生成电池包'):
        result = generate_battery_pack()
        http = {
            "host": env['host']['tsp_in'],
            "path": create_battery_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ""
            },
            "json": {'requestMsg': result['battery_data']}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
    with allure.step('在数据库中绑定车和电池，预换电车即只设置pre_new_code'):
        mysql['battery_trace'].delete('sys_veh', {'vin': vin})
        data = {'vin': vin, 'vehicle_id': vid, 'code': result['gbt_code'], 'license_plate': None,
                'veh_model_name': None, 'veh_config': None, 'manufacturing_date': None, 'sale_time': None,
                'sale_area': None, 'owner_name': None, 'epname': None,'epaddress': None, 'create_time': None,
                'update_time': None, 'report_time': None,'veh_cert_print_date': None, 'Idnum': None, 'epcode': None,
                'veh_type_name': None, 'status': 0, 'shanghai_status': 1, 'account_id': 0, 'message': None,
                'new_code': None, 'pre_new_code': None, 'user_name': None}
        mysql['battery_trace'].insert('sys_veh', data)
    yield result
    with allure.step('测试完成后删除创建的电池数据'):
        mysql['battery_trace'].delete('sys_battery_pack_entity', {'code': result['gbt_code']})
        mysql['battery_trace'].delete('sys_battery_module_entity', {'pack_id': result['gbt_code']})
        mysql['battery_trace'].delete('sys_veh', {'vin': vin})


def test_get_change_vehicle_status(env, mysql):
    vin = env['vehicles']['colin']['vin']
    status = random.choice([-1, 1, 2, 3, 4, 5])
    with allure.step(f'修改车辆{vin}的状态为{status}'):
        http = {
            "host": env['host']['tsp_in'],
            "path": change_vehicle_status_path,
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
                "vin": vin,
                "status": status
            },
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
    with allure.step(f'在db中校验status已经被改为{status}'):
        record = mysql['battery_trace'].fetch_one('sys_veh', {'vin': vin})
        assert_equal(record['status'], status)
