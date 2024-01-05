#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2022/01/07 11:30
@contact: hongzhen.bi@nio.com
@api: POST_/api/1/in/hermes/ecall/register
@api: POST_/api/1/in/hermes/ecall/feedback
@description: E-Call Event Register and FeedBack
@showdoc: http://showdoc.nevint.com/index.php?s=/150&page_id=32905
@showdoc: http://showdoc.nevint.com/index.php?s=/150&page_id=32906
@consumer: rvs_server
"""
import time

import allure

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


class TestEcallPushNctAck(object):
    """
                                                                                                    push CVS
                                                             ----/api/1/in/hermes/ecall/register-----   ⬆
                                                            |                                        ⬇
    Ecall_event -> NMP -> kafka(10005-data_report) -> rvs_server -> kafka(80001-ecall)    ----->    hermes -> test_ecall_alert.py
                                                                                |                       ⬆
                                                                                |                 remote_vehicle(api:feedback)
                                                                                |                       ⬆
                                                                                 -> NCT(要求1min内ack) --
                                                                                |                       ⬆
                                                                                 -> SCR(要求5min内ack) --
    """

    def test_ecall_push_nct_ack(self, env, vid, cmdopt, mysql, redis, publish_msg_by_kafka):
        """
        config_map:
            ecall.alarm.notify.check = true
            ecall.alarm.phase1.minute.gap = 1
            ecall.alarm.phase2.minute.gap = 5

        接收者redis key: hermes_test:ecall_alarm_notify_recipient
            hget hermes_test:wti_notify_recipient 13888888888
            > xxx@nio.com
        """
        key = f"hermes_{cmdopt}:ecall_alarm_notify_recipient"
        with allure.step("首先添加要推送的员工"):
            redis['cluster'].hash_set(key, '15911051120', 'hongzhen.bi@nio.com')
        with allure.step("rvs_server调hermes接口，向hermes注册ecall事件，存到ecall_alarm"):
            event_id = int(time.time())
            inputs = {
                "host": env['host']['tsp_in'],
                "path": "/api/1/in/hermes/ecall/register",
                "method": "POST",
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "params": {
                    'app_id': '80001',
                    'sign': ''
                },
                "data": {
                    "vehicle_id": vid,
                    "event_id": event_id,
                    "sample_ts": int(time.time() * 1000),
                }
            }
            response = hreq.request(env, inputs)
            time.sleep(2)
            # hermes register接口内直接起线程等待1min和5min的触发，和ecall事件的时间戳无关
            mysql_data = mysql['hermes'].fetch("ecall_alarm", where_model={"vehicle_id": vid, "event_id": event_id})
            assert_equal(len(mysql_data), 1)
            assert_equal(mysql_data[0]['status'], 0)
        with allure.step("校验返回成功"):
            assert response["result_code"] == "success"
        with allure.step("1min内没有收到NCT调用feedback返回的ack，则推送CVS"):
            # 验证收到短信和邮件
            pass
        with allure.step("5min内没有收到SCR调用feedback返回的ack，则推送CVS"):
            # 验证收到短信和邮件
            pass

    def test_ecall_not_push_nct_ack(self, env, vid, cmdopt, mysql, redis, publish_msg_by_kafka):
        key = f"hermes_{cmdopt}:ecall_alarm_notify_recipient"
        with allure.step("首先添加要推送的员工"):
            redis['cluster'].hash_set(key, '15911051120', 'hongzhen.bi@nio.com')
        with allure.step("rvs_server调hermes接口，向hermes注册ecall事件，存到ecall_alarm"):
            event_id = int(time.time())
            inputs = {
                "host": env['host']['tsp_in'],
                "path": "/api/1/in/hermes/ecall/register",
                "method": "POST",
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "params": {
                    'app_id': '80001',
                    'sign': ''
                },
                "data": {
                    "vehicle_id": vid,
                    "event_id": event_id,
                    "sample_ts": int(time.time() * 1000),
                }
            }
            response = hreq.request(env, inputs)
            time.sleep(2)
            # hermes register接口内直接起线程等待1min和5min的触发，和ecall事件的时间戳无关
            mysql_data = mysql['hermes'].fetch("ecall_alarm", where_model={"vehicle_id": vid, "event_id": event_id})
            assert_equal(len(mysql_data), 1)
            assert_equal(mysql_data[0]['status'], 0)
        with allure.step("校验返回成功"):
            assert response["result_code"] == "success"
        with allure.step("1min内收到NCT调用feedback返回的ack，则不推送CVS"):
            # 验证收到短信和邮件
            time.sleep(3)
            self._ack(env, vid, event_id, 1)
            mysql_data = mysql['hermes'].fetch("ecall_alarm", where_model={"vehicle_id": vid, "event_id": event_id})
            assert_equal(mysql_data[0]['status'], 1)
        with allure.step("5min内收到SCR调用feedback返回的ack，则不推送CVS"):
            # 验证收到短信和邮件
            time.sleep(63)
            self._ack(env, vid, event_id, 2)
            mysql_data = mysql['hermes'].fetch("ecall_alarm", where_model={"vehicle_id": vid, "event_id": event_id})
            assert_equal(mysql_data[0]['status'], 2)
        with allure.step("删除redis"):
            redis['cluster'].hash_hdel(key, "15911051120")


    def _ack(self, env, vid, event_id, status):
        """
        接口中控制了只有比DB中存储的 status 大才会更新
        """
        inputs = {
            "host": env['host']['tsp_in'],
            "path": "/api/1/in/hermes/ecall/feedback",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                'app_id': '80001',
                'sign': ''
            },
            "data": {
                "vehicle_id": vid,
                "event_id": event_id,
                "status": status,
                "sample_ts": int(time.time() * 1000),
            }
        }
        response = hreq.request(env, inputs)
        with allure.step("校验返回成功"):
            assert response["result_code"] == "success"
