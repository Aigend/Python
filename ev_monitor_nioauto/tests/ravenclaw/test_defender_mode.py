#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2022/06/07 10:44
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


class TestDefenderMode(object):
    """
    守卫模式fds: https://nio.feishu.cn/wiki/wikcnUfeT7SIAvm1JVbnuYmvkyU
    APP PRD: https://nio.feishu.cn/wiki/wikcnG7z6z91EimwMvZGVmklCTf#LEqKv6

    CDC ---> data_report (/api/1/data/report) ---> kafka (swc-tsp-data_report-{env}-100648-hu_data_report) ---> ravenclaw ---> MySQL (vehicle_offcar_mode_status)
                                                                                                                 |   |
                                                                              Push车主和操作者的APP (reason!=0)<---     ---> Redis (remote_vehicle_{env}:vehicle_status:{vid}:VehicleOffcarModeStatus)
                                                                                                                            |
                                                                                                            APP ---> remote_vehicle (status接口查询offcar_mode_status)
    注意:
        1、data_reoprt的数据上报接口是通用功能，该接口的数据会推送到events参数内app_id对应的hu_data_report kafka中
        2、非激活的车不推送
        3、文案语言调account获取，存redis一天

    6/24需求宣讲：
        0. 增加激活状态
        1. 谁开的谁才能关，主用车人可以关所有
        2. 告警日志
        3. 实况画面的权限有无放在哪里来查和返回
        4. 消息提醒，加入AES秘钥，跳转到获取二维码页面（如果APP本地没有存）
    """

    def test_defender_mode(self, env, vid, mysql, redis):
        with allure.step("调用/api/1/data/report接口上报宠物模式"):
            defender_event = random.choice(range(16))
            # defender mode status  0 关 1 开 2 报警中
            if defender_event in [0, 6, 7, 8, 9]:
                defender_mode_status = 0
            elif defender_event == 1:
                defender_mode_status = 1
            elif defender_event in [3, 4, 5]:
                defender_mode_status = 2
            else:
                defender_mode_status = None
            """
                0      // 守卫模式关闭
                1      // 守卫模式打开
                2      // 守卫模式激活
                3      // 守卫模式一级报警触发
                4      // 守卫模式二级报警触发
                5      // 守卫模式三级报警触发
                6      // 守卫模式退出：系统异常
                7      // 守卫模式退出：上高压失败
                8      // 守卫模式退出：续航里程过低
                9      // 守卫模式退出：其他原因
                10     // 守卫模式通知：续航里程较低
                11     // 守卫模式通知：系统内存异常
                12     // 守卫模式通知：系统存储故障
                13     // 守卫模式通知：后视镜折叠，守卫模式效果受限
                14     // 守卫模式通知：环视摄像头异常
                15     // 守卫模式通知：座舱摄像头异常
            """
            timestamp = int(time.time() * 1000)
            events = [
                {
                    "app_id": "100648",
                    "app_ver": "1.0.82.01",
                    "timestamp": timestamp,
                    "event_type": "defender",
                    "defender_event": defender_event,
                    "remote": 1,    # 0是车机开启，1是远程开启
                    "time": timestamp
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
                    'user_id': 402355066,
                    'vid': vid,
                    'events': json.dumps(events)
                }
            }
            response = hreq.request(env, inputs)
            logger.info("request status is {}".format(response["result_code"]))
        with allure.step("校验RDS"):
            if defender_mode_status:
                time.sleep(3)
                date_time = time_sec_to_strtime(timestamp / 1000)
                data = mysql['rvs'].fetch('vehicle_offcar_mode_status', {'id': vid})[0]
                assert_equal(data['defender_mode'], defender_mode_status)
                assert_equal(data['defender_mode_et'], date_time)
        with allure.step("校验redis"):
            if defender_mode_status:
                key = f'remote_vehicle_test:vehicle_status:{vid}:VehicleOffcarModeStatus'
                redis_data = json.loads(redis['cluster'].get(key))
                assert_equal(redis_data['defender_mode'], defender_mode_status)
                assert_equal(redis_data['defender_mode_event_time'], int(timestamp / 1000))

        # 查log推送记录，消息标题：守卫模式
        """
        需要app推送的defender_event: 4, 5, 6, 7, 8, 9, 10, 13, 14
        需要sms推送的defender_event: 4, 5
        """
