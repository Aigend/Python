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
from urllib3 import encode_multipart_formdata


def test_data_logger_mutli_upload_init(env, mysql):
    """
        https://nio.feishu.cn/docs/doccngR24LsBEUXNm6tV3kDbSeg#
    "upload_id": "1623145288f5d589a4b1728c1e31fab13777301ee7b019a299e02c9e369aaa9abc11ac9a62",
    "key": "test/bd2_003/normal_file/test_upload1.mp4"
    """

    app_id = 100466
    inputs = {
        "host": env['host']['tsp_ex'],
        "path": "/api/1/phoenix/upload/mutli_upload_init",
        "method": "POST",
        "params": {
            "app_id": app_id,
            "sign": ""
        },
        "data": {
            "device_token": "10f5767b-f879-4410-bb57-606c531d6c6b",
            "device_sn": "bd2_003",
            "file_name": "test_upload.mp4",
        },
        "files": {"file": ""}  # 加这是为了data不参与签名，勿删
    }
    response = hreq.request(env, inputs)
    logger.debug(f"response {response}")
    assert response['result_code'] == 'success'
