#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2022/05/31 20:01
@contact: hongzhen.bi@nio.com
"""
import json
import random
import time

import allure

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.time_parse import time_sec_to_strtime


class TestPetMode(object):
    """
    宠物模式PRD: https://nio.feishu.cn/docs/doccnFf2wlqRhRz0prkebmJbyee
    SRD: https://nio.feishu.cn/docs/doccnyE0N6LqfiM24V3wyCDm3Yg

    CDC ---> data_report (/api/1/data/report) ---> kafka (swc-tsp-data_report-{env}-30003-hu_data_report) ---> ravenclaw ---> MySQL (vehicle_offcar_mode_status)
                                                                                                                 |   |
                                                                              Push车主和操作者的APP (reason!=0)<---     ---> Redis (remote_vehicle_{env}:vehicle_status:{vid}:VehicleOffcarModeStatus)
                                                                                                                            |
                                                                                                            APP ---> remote_vehicle (status接口查询offcar_mode_status)
    注意:
        1、data_reoprt的数据上报接口是通用功能，该接口的数据会推送到events参数内app_id对应的hu_data_report kafka中
        2、非激活的车不推送
        3、文案语言调account获取，存redis一天
    """

    def test_pet_mode(self, env, vid, mysql, redis):
        """
        event_type:
            Setting_PetMode_Enter   进入宠物模式
            Setting_PetMode_Exit    退出宠物模式      reason  0x0-正常退出;0x1-预留;0x2-里程小于10KM;0x3-高压故障;0x4-空调故障;0x5-电池起火故障
                                                            0x7-里程小于10KM，激活失败;0x8-高压故障，激活失败;0x9-空调故障，激活失败;0x10-电池起火故障，激活失败
            Setting_PwrHoldMd_Enter 进入离车保持模式
            Setting_PwrHoldMd_Exit  退出离车保持模式   reason  0x0-正常退出;0x1-计时到期;0x2-里程小于10KM;0x3-高压故障;0x4-空调故障;0x5-电池起火故障
            Setting_CampMd_Enter    进入露营模式
            Setting_CampMd_Exit     退出露营模式      reason  0x0-正常退出;0x1-预留;0x2-里程小于10KM;0x3-高压故障;0x4-空调故障;0x5-电池起火故障
        """
        with allure.step("调用/api/1/data/report接口上报宠物模式"):
            modes = [
                {"pet_mode": "Setting_PetMode"},
                {"power_hold_mode": "Setting_PwrHoldMd"},
                {"camping_mode": "Setting_CampMd"}
            ]

            index = random.randrange(len(modes))
            enter_mode = modes.pop(index)
            enter_mode_key = list(enter_mode.keys())[0]
            enter_mode_value = list(enter_mode.values())[0]
            event_type_enter = enter_mode_value + "_Enter"

            exit_mode = random.choice(modes)
            exit_mode_key = list(exit_mode.keys())[0]
            exit_mode_value = list(exit_mode.values())[0]
            event_type_exit = exit_mode_value + "_Exit"
            reason = random.choice([0, 1, 2, 3, 4, 5, 7, 8, 9, 10])

            timestamp = int(time.time() * 1000)
            events = [
                {
                    "app_id": "30003",
                    "app_ver": "1.0.82.01",
                    "timestamp": timestamp,
                    "event_type": event_type_enter,
                    "time": timestamp
                },
                {
                    "app_id": "30003",
                    "app_ver": "1.0.82.01",
                    "timestamp": timestamp,
                    "event_type": event_type_exit,
                    "time": timestamp,
                    "reason": reason,
                    "user_id": 402355066

                }
            ]
            inputs = {
                "host": env['host']['tsp'],
                "path": "/api/1/data/report",
                "method": "POST",
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "params": {
                    'app_id': '10000',
                    'sign': ''
                },
                "data": {
                    "model": 'ES8',
                    "os": 'android',
                    'os_ver': '1.0.0',
                    'os_lang': 'unknown',
                    'os_timezone': 'unknown',
                    'network': 'unknown',
                    "client_timestamp": timestamp,
                    'vid': vid,
                    'events': json.dumps(events)
                }
            }
            response = hreq.request(env, inputs)
            logger.info("request status is {}".format(response["result_code"]))
        with allure.step("校验RDS"):
            time.sleep(3)
            date_time = time_sec_to_strtime(timestamp / 1000)
            data = mysql['rvs'].fetch('vehicle_offcar_mode_status', {'id': vid})[0]
            assert_equal(data[enter_mode_key], 1)
            assert_equal(data[enter_mode_key + '_et'], date_time)
            assert_equal(data[exit_mode_key], 0)
            assert_equal(data[exit_mode_key + '_et'], date_time)
        with allure.step("校验redis"):
            key = f'remote_vehicle_test:vehicle_status:{vid}:VehicleOffcarModeStatus'
            redis_data = json.loads(redis['cluster'].get(key))
            assert_equal(redis_data[enter_mode_key], 1)
            assert_equal(redis_data[enter_mode_key + '_event_time'], int(timestamp / 1000))
            assert_equal(redis_data[exit_mode_key], 0)
            assert_equal(redis_data[exit_mode_key + '_event_time'], int(timestamp / 1000))

        # 查log推送记录，消息标题：宠物模式已退出 or 离车不下电模式已退出 or 露营模式已退出
