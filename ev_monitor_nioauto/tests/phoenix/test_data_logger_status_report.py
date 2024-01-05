# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_datalogger_status_report.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/3 11:15 上午
# @Description :

import time
import pytest
import allure
import json
import random
from utils.http_client import TSPRequest as hreq
from utils.logger import logger


def test_data_logger_status_report(env, mysql):
    """
        https://nio.feishu.cn/docs/doccngR24LsBEUXNm6tV3kDbSeg#
    """
    app_id = 100466
    list = [{"part_number": 1, "e_tag": "435a9fa61ada62950d14d28612c36600"},
            {"part_number": 2, "e_tag": "1994d124705a5d1e715fa14d3777090c"},
            {"part_number": 3, "e_tag": "dccd13fffa9bb4bd76532857868623fb"},
            {"part_number": 4, "e_tag": "834395c06c7d6c7d40f073ce7cad8963"}]
    status_report = {
        "network_connection_status": 1,
        "network_signal_strength": 3,
        "network_connection_name": "4G",
        "pad_running_status": 1,
        "datalogger_running_status": 1,
        "storage_running_status": 2,
        "storage_total_size": 300,
        "storage_free_size": 200,
        "data_upload_status": 1,
        "gps_running_status": 1,
        "gps_longitude": 114.4,
        "gps_latitude": 30.6,
        "pad_working_voltage": 4.6,
        "pad_working_temperature": 25.6,
        "datalogger_working_voltage": 3.5,
        "datalogger_working_temperature": 25.6
    }
    inputs = {
        "host": env['host']['tsp_ex'],
        "path": "/api/1/phoenix/datalogger/status_report",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "params": {
            "app_id": app_id,
            "sign": ""
        },
        "json": {
            "device_token": "10f5767b-f879-4410-bb57-606c531d6c6b",
            "device_sn": "bd2_003",
            "status_report": json.dumps(status_report),
            "sample_time": int(time.time()),
        }
    }
    response = hreq.request(env, inputs)
    logger.debug(f"response {response}")
    assert response['result_code'] == 'success'
    # message_id = response['data']['message_id']
    # with allure.step("校验mysql"):
    #     email_history = mysql['nmp_app'].fetch('email_history', {'message_id': message_id}, ['recipient'])
    #     recipient_list = recipients.split(',')
    #     for email_history_info in email_history:
    #         assert (email_history_info['recipient'] in recipient_list) == True
    #     email_content = mysql['nmp_app'].fetch('email_history_meta_info', {'message_id': message_id})
    #     assert len(email_content) == 1
