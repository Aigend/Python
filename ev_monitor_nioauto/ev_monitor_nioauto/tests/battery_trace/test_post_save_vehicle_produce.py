# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:qiangwei.zhang
@time: 2022/05/31
@api: POST_/api/1/in/battery/save_vehicle_produce
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=34063
@description: 保存车辆生产信息
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal
from utils.random_tool import generate_random_gbt_code
from utils.time_parse import now_utc_strtime

g_model_id = "HFC6483ECEV-W"
g_config_id = "HFC6483ECEV-W"
g_vin = "SQETEST0777701324"
g_vehicle_id = "b8f6b4163158427a9009dc9db2d83c16"
g_make_date = now_utc_strtime('%Y-%m-%d', -3600 * 24)
g_cert_print_date = now_utc_strtime('%Y-%m-%d', -3600 * 24 * 3)
g_code_id = generate_random_gbt_code('03U', 'P')
g_veh_cert_num = "2022veh cert num"


save_vehicle_produce_keys = 'case_name,code,vin,vehicle_id,veh_make_date,veh_cert_num,veh_cert_print_date,veh_model_id,veh_config_id'
save_vehicle_produce_cases = [
    ("正案例_正常请求参数", g_code_id, g_vin, g_vehicle_id, g_make_date, g_veh_cert_num, g_cert_print_date, g_model_id, g_config_id),
    ("反案例_code为None", None, g_vin, g_vehicle_id, g_make_date, g_veh_cert_num, g_cert_print_date, g_model_id, g_config_id),
    ("反案例_vin为None", g_code_id, None, g_vehicle_id, g_make_date, g_veh_cert_num, g_cert_print_date, g_model_id, g_config_id),
    ("反案例_vehicle_id为None", g_code_id, g_vin, None, g_make_date, g_veh_cert_num, g_cert_print_date, g_model_id, g_config_id),
    ("反案例_veh_make_date为None", g_code_id, g_vin, g_vehicle_id, None, g_veh_cert_num, g_cert_print_date, g_model_id, g_config_id),
    ("反案例_veh_cert_num为None", g_code_id, g_vin, g_vehicle_id, g_make_date, None, g_cert_print_date, g_model_id, g_config_id),
    ("反案例_veh_cert_print_date为None", g_code_id, g_vin, g_vehicle_id, g_make_date, g_veh_cert_num, None, g_model_id, g_config_id),
    ("反案例_veh_model_id为None", g_code_id, g_vin, g_vehicle_id, g_make_date, g_veh_cert_num, g_cert_print_date, None, g_config_id),
    ("反案例_veh_config_id为None", g_code_id, g_vin, g_vehicle_id, g_make_date, g_veh_cert_num, g_cert_print_date, g_model_id, None),
]
save_vehicle_produce_ids = [f"{case[0]}" for case in save_vehicle_produce_cases]


@pytest.mark.skip('deprecated')
@pytest.mark.parametrize(save_vehicle_produce_keys, save_vehicle_produce_cases, ids=save_vehicle_produce_ids)
def test_post_save_vehicle_produce(env, cmdopt, mysql, case_name, code, vin, vehicle_id, veh_make_date, veh_cert_num, veh_cert_print_date, veh_model_id, veh_config_id):
    app_id = 100078
    with allure.step('添加车辆公告号'):
        json = {
            'code': code,
            'vin': vin,
            'vehicle_id': vehicle_id,
            'veh_make_date': veh_make_date,
            'veh_cert_num': veh_cert_num,
            'veh_cert_print_date': veh_cert_print_date,
            'veh_model_id': veh_model_id,
            "veh_config_id": veh_config_id
        }
        json = {k: v for k, v in json.items() if v is not None}
        inputs = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/save_vehicle_produce',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": json
        }
        response = restClient.request(env, inputs)
    with allure.step('校验结果'):
        if case_name.startswith("正案例"):
            assert_equal(response['result_code'], "success")
            record = mysql['battery_trace'].fetch_one('sys_veh', {'code': code})
            assert record["vin"] == vin
            assert record["vehicle_id"] == vehicle_id
            assert record["code"] == code
            assert record["new_code"] == code
            assert record["pre_new_code"] == code
            assert record["manufacturing_date"] == f"{veh_make_date} 00:00:00"
            assert record["veh_cert_print_date"] == f"{veh_cert_print_date} 00:00:00"
            assert record["veh_model_name"] == veh_model_id
            assert record["veh_config"] == veh_config_id
        else:
            assert_equal(response['result_code'], "internal_error")
