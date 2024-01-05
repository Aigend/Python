#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/13 12:01
@contact: li.liu2@nio.com
@description:
    TSP Agent 命令下发
    http://showdoc.nevint.com/index.php?s=/13&page_id=359


    * 车控命令接口调用该接口给车机下发指令
    * 该接口不会等待车机的回应再返回，message_state状态变为1就返回success
    * 如果车机CGW不在线，则message_state只有1值，否则有1，2501，5001，10000四值。该命令在CGW重在线后，不会补推信息。不像notify_hu命令在CDC不在线的时候会入队（2501）且CDC重在线会补推。
    * 支持按照Device ID 发送命令
    * 支持回调URL，当消息到达客户端的时候，调用此URL
    * 支持Base64 编码消息，不对消息进行解析。
    # allow_app_id:["80001","10011","100557"] venus配置文件控制

"""
import json
import time

import allure
import pytest

from tests.tsp_message_center.vehicle_online import vehicle_online
from utils.assertions import assert_equal
from utils.httptool import request as rq
from utils.http_client import TSPRequest as hreq
from config.cert import web_cert, web_cert_alps, alps_in_ca_chain, web_cert_mp
from utils.logger import logger


class TestMeesageAPI(object):
    command_keys = "case_name,origin_app_id,target_app_id,platform,ecu"
    command_cases = [
        ["NT1_CGW_COMMAND", '80001', 10005, "NT1", "cgw"],
        ["NT1_ADC_COMMAND", '80001', 10107, "NT1", "adc"],
        ["NT2_CGW_COMMAND", '80001', 10005, "NT2", "sa"],
        ["NT2_ADC_COMMAND", '80001', 100512, "NT2", "adc_nt2"],
        ["NT1_CGW_COMMAND", '10011', 10005, "NT1", "cgw"],
        ["NT2_ADC_COMMAND", '100557', 100512, "NT2", "adc_nt2"],
    ]
    command_ids = [f"{case[1]} {case[0]}" for case in command_cases]

    @pytest.mark.parametrize(command_keys, command_cases, ids=command_ids)
    def test_command(self, env, cmdopt, mysql, case_name, target_app_id, origin_app_id, platform, ecu):
        """
        TSP Agent 命令下发
        http://showdoc.nevint.com/index.php?s=/13&page_id=359
        """
        # allow_app_id:["80001","10011","100557"] venus配置文件控制
        if origin_app_id == "100557" and "marcopolo" in cmdopt:
            logger.debug(f"eu 环境无100557app_id")
            return 0

        host_tsp_in = env['host']['tsp_in']
        vehicle_id = env['vehicles']['register_client'][platform]['v1']["vid"]
        client_id = env['vehicles']['register_client'][platform]['v1'][f"{target_app_id}_client"]

        with allure.step(f"使{vehicle_id}在线"):
            online_result = vehicle_online(env, vehicle_id, ecu)
        with allure.step(f"命令下发接口:{case_name}"):
            inputs = {
                "host": host_tsp_in + ':4430',
                "path": "/api/1/sec/in/message/command",
                "method": "POST",
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": origin_app_id,
                    "sign": ""
                },
                "data": {
                    'nonce': str(int(time.time() * 1000)),
                    'scenario': 'rvs_set_doorlock',
                    'device_ids': vehicle_id,
                    'ttl': 10000,
                    'target_app_id': target_app_id,
                    'payload': json.dumps(
                        {"command_id": 93229391, "doorlock": 1, "max_duration": "20", "key": json.dumps({"command_id": 93229391, "doorlock": 1, "max_duration": "20"})}),
                },
                "verify": False,
                "cert": web_cert_mp if "marcopolo" in cmdopt else web_cert
            }
            response = hreq.request(env, inputs)
            time.sleep(2)
        with allure.step(f"校验命令下发接口:{case_name}"):
            assert response["result_code"] == "success"
            message_id = response['data'].get("message_id")
            res_expect = {
                "data": {
                    "details": [
                        {
                            "client_id": client_id,
                            "result": "success",
                            "device_id": vehicle_id,
                            "user_id": 0,
                            "app_id": str(target_app_id)
                        }
                    ],
                    "message_id": message_id,
                },
                "success": 1,
                "failure": 0,
                "result_code": "success",
                "request_id": response.get('request_id'),
                "server_time": response.get('server_time'),

            }
            assert_equal(response, res_expect)
            with allure.step('校验数据库message_test_tsp的message_state表'):
                message_results = mysql['nmp'].fetch('message_state', where_model={'message_id': message_id}, fields=['state'], suffix="order by state")
                expect = [{'state': 1}, {'state': 2501}, {'state': 5001}, {'state': 10000}]
                if online_result:
                    assert_equal(message_results, expect)
                else:
                    assert_equal(message_results[0], expect[0])


@pytest.mark.skip("alps")
def test_command_alps(env, mysql):
    """
    TSP Agent 命令下发
    http://showdoc.nevint.com/index.php?s=/13&page_id=359
    """
    host_tsp_in = env['host']['tsp_in']
    user = 'nmp'
    client_id = env['vehicles'][user]['client_id']
    vehicle_id = "7930bdfe7538486aabecedc336ef383c"
    command_id = 93229391 if user == 'nmp' else 90390704  # li is 90390704
    with allure.step('验证command接口'):
        inputs = {
            "host": host_tsp_in + ':4430',  # 4430双向认证，443单向认证
            "path": "/api/1/sec/in/message/command",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": '10011',
                # allow_app_id:["80001","10011","100557"] venus配置文件控制
                "sign": ""
            },
            "data": {
                'nonce': 'nondceafadfdasfadfa',
                'scenario': 'rvs_set_doorlock',
                'device_ids': vehicle_id,
                'ttl': 10000,
                'target_app_id': 10005,
                # command_id 需要是一个vehicle control 产生的comamnd_id
                # doorlock 1 关，2 开，  对应status_door表vehicle_lock_status 1 全关，0 开
                'payload': json.dumps({"command_id": command_id, "doorlock": 1, "max_duration": "20"})
            },
            "verify": False,
            "cert": web_cert_alps,
        }
    response = hreq.request(env, inputs)
    assert response["result_code"] == "success"
    message_id = response['data']['message_id']
    # time.sleep(2)
    # with allure.step('校验数据库message_test_tsp的message_state表'):
    #     message_results = mysql['nmp'].fetch('message_state', where_model={'message_id': message_id}, fields=['state'])
    #     # assert len(message_results)>0
    #     # TODO 让车辆在线
    #     expect = [{'state': 1}, {'state': 2501}, {'state': 5001}, {'state': 10000}]
    #     assert_equal(message_results[0], expect[0])
