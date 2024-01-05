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
        device_token
device_type
device_sn
file_type
file_name
file_size
remote_path
start_time
end_time
extend_info
    """
    # test/bd2_001/normal_file/test.mp4

    app_id = 100466
    device_token = "10f5767b-f879-4410-bb57-606c531d6c6b"
    device_sn = "bd2_003"
    remote_path = "test/bd2_003/normal_file/28M视频文件.mp4"
    file_type = "mp4"
    file_name = "test.mp4"
    file_size = 28 * 1000 * 1024
    extend_info = {
        "msg": "测试使用extend_info",
    }
    inputs = {
        "host": env['host']['tsp_ex'],
        "path": "/api/1/phoenix/upload/file_upload_notice",
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "params": {
            "app_id": app_id,
            "sign": ""
        },
        "json": {
            "device_token": device_token,
            "device_type": "datalogger",
            "device_sn": device_sn,
            "file_type": file_type,
            "file_name": file_name,
            "file_size": file_size,
            "remote_path": remote_path,
            "start_time": int(time.time()) - 360,
            "end_time": int(time.time()),
            "extend_info": json.dumps(extend_info),
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
