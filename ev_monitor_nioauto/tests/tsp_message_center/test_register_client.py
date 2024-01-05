#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:qiangwei.zhang
@time: 2022/04/02 16:30
@contact: qiangwei.zhang@nio.com
@description:
    注册client_id
    http://showdoc.nevint.com/index.php?s=/13&page_id=1070
    tsp_unique_client_white_list:10005,10107
"""
import time
import allure
import pytest
from config.settings import tsp_vehicle_auth
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


class TestMessageAPI(object):
    register_client_keys = "case_name,app_id,platform,ecu,host_name"
    register_client_cases = [
        # NT1 车辆
        ["NT1_CGW注册client", 10005, "NT1", 'cgw', "v_in_4430"],
        ["NT1_ADC注册client", 10107, "NT1", 'adc', "v_in_4430"],
        # NT2 车辆
        ["NT2_SA注册client", 10005, "NT2", 'sa', "v_in_4430"],
        ["NT2_ADC注册client", 100512, "NT2", 'adc', "adc_ex_4430"],
    ]
    register_client_ids = [f"{case[0]}" for case in register_client_cases]

    @pytest.mark.parametrize(register_client_keys, register_client_cases, ids=register_client_ids)
    def test_register_client(self, env, cmdopt, mysql, case_name, app_id, platform, ecu, host_name):
        # 用不同的车绕过频率控制
        with allure.step("注册client接口"):
            vehicle_key = 'v2' if platform == "NT1" and app_id == 10107 else "v1"
            vehicle_id = env['vehicles']['register_client'][platform][vehicle_key]["vid"]
            vehicle_cert = tsp_vehicle_auth(cmdopt, vehicle_id, platform)
            inputs = {
                "host": env['host'][host_name],
                "path": "/api/1/message/register_client",
                "method": "POST",
                "headers": {'Content-Type': 'application/x-www-form-urlencoded'},
                'params': {
                    'app_id': app_id,
                    'region': 'cn',
                    'lang': 'zh_cn',
                    'sign': '',
                },
                'data': {
                    'app_version': '1.3.4',
                    'brand': 'xiaomi',
                    'device_type': 'vehicle',
                    'device_token': '',
                    'device_id': vehicle_id,
                    'os': 'android',
                    'os_version': '6.0',
                    'nonce': str(int(time.time() * 1000))
                },
                "verify": False,
                "cert": vehicle_cert.get(f"{ecu}_cert"),
            }
            response = hreq.request(env, inputs)
        with allure.step("校验结果"):
            assert response['result_code'] == "success"
            db_res = mysql['nmp'].fetch("clients", {"device_id": vehicle_id, "app_id": app_id})
            client_id = db_res[0].get("client_id")
            expect_res = {"data": {"client_id": client_id}, "result_code": "success", }
            response.pop("request_id")
            response.pop("server_time")
            assert_equal(response, expect_res)
