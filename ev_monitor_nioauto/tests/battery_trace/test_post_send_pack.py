# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author: qiangwei.zhang
@time: 2022/03/10
@api: GET_/api/1/in/battery/send_pack
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=33513
@description: 推送简易的包信息到t-common-kafka集群，topic是 ds-battery-trace-test-pack
test kafka : http://10.125.234.253:60080/clusters/t-common-kafka/topics/ds-battery-trace-test-pack
"""
import random

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.logger import logger
from utils.random_tool import generate_battery_add_info, generate_battery_pack
from utils.assertions import assert_equal


@pytest.fixture(autouse=True)
def prepare_battery_code(env, mysql):
    with allure.step('测试开始前生成电池扩展信息数据'):
        # result = generate_battery_pack(logistic_des=101)
        logistic_des = random.choice([101, 102, 103])  # 101 - 生产库, 102 - 售后库, 103 - 换电库
        result = generate_battery_pack(logistic_des=logistic_des)
    with allure.step('生成电池模组'):
        app_id = 100078
        http = {
            "host": env['host']['tsp_in'],
            "path": "/api/1/in/battery/receiveBatteryProduce",
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
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
    with allure.step('校验电池包在db中已经创建'):
        record = mysql['battery_trace'].fetch('sys_battery_pack_entity', {'code': result['gbt_code']})
        assert_equal(len(record), 1)
        yield record, logistic_des
    # with allure.step('测试完成后删除创建的模组电池数据'):
    #     mysql['battery_trace'].delete('sys_battery_module_entity', {'pack_id': result['gbt_code']})


def test_get_send_pack(env, prepare_battery_code, kafka):
    kafka['comn'].set_offset_to_end(kafka['topics']['battery_pack'])
    with allure.step('推送电池包信息到kafka'):
        app_id = 100078
        record, logistic_des = prepare_battery_code
        code = record[0]['code']
        nio_encoding = record[0]['nio_encoding']
        http = {
            "host": env['host']['tsp_in'],
            "path": "/api/1/in/battery/send_pack",
            "method": "GET",
            "params": {
                "app_id": app_id,
                # "code": code,
                "nio_encoding": nio_encoding,
                "sign": ""
            }
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
    with allure.step('校验response'):
        response.pop("server_time")
        response.pop("request_id")
        expected_res = {
            "result_code": "success",
            "debug_msg": "",
            "data": None
        }
        assert_equal(response, expected_res)
        with allure.step('校验kafka'):
            expected_data = {"code": code, "nio_encoding": nio_encoding, "logistic_des": logistic_des}
            datas = kafka['comn'].consume(kafka['topics']['battery_pack'], timeout=10)
            for data in datas:
                logger.debug(f"kafka data {data}")
                data_dict = eval(data)
                assert_equal(data_dict, expected_data)
                logger.debug(f"{data_dict}")
