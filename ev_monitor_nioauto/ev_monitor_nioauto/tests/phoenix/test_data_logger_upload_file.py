# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_datalogger_status_report.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/3 11:15 上午
# @Description :


import time
import json
import os
import allure
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from urllib3 import encode_multipart_formdata
import requests


def test_data_logger_upload_file(env, mysql):
    """
        https://nio.feishu.cn/docs/doccngR24LsBEUXNm6tV3kDbSeg#
        "Content-Type": "multipart/form-data",
    """
    with allure.step("文件上传初始化接口"):
        file_path = "./new_t3_road.txt"
        file_name = os.path.basename(file_path)
        file_type = file_name.split('.')[-1]
        file_size = os.path.getsize(file_path)
        app_id = 100466
        inputs = {
            "host": env['host']['tsp_ex'],
            "path": "/api/1/phoenix/upload/upload_file",
            "method": "POST",
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "data": {
                "device_token": "10f5767b-f879-4410-bb57-606c531d6c6b",
                "device_sn": "bd2_003",
                "file_name": file_name,
            },
            "files": {"file": open(file_path, "rb")},
        }
        response = hreq.request(env, inputs)
        logger.debug(f"response {response}")
        assert response['result_code'] == 'success'
        remote_path = response.get("data")
    with allure.step("文件上传成功通知接口"):
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
                "device_token": "10f5767b-f879-4410-bb57-606c531d6c6b",
                "device_type": "datalogger",
                "device_sn": "bd2_003",
                "file_type": file_type,
                "file_name": file_name,
                "file_size": file_size,
                "remote_path": remote_path,
                "start_time": int(time.time()) - 360,
                "end_time": int(time.time()),
                "extend_info": json.dumps({"msg": "测试使用extend_info",}),
            }
        }
        response = hreq.request(env, inputs)
        logger.debug(f"response {response}")
        assert response['result_code'] == 'success'