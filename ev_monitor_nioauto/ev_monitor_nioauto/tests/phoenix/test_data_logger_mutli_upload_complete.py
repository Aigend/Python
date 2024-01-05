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


def test_data_logger_mutli_upload_complete(env):
    """
        https://nio.feishu.cn/docs/doccngR24LsBEUXNm6tV3kDbSeg#
        device_token
        device_sn
        upload_id
        key
        etags

    """

    app_id = 100466
    data = {'device_token': '10f5767b-f879-4410-bb57-606c531d6c6b',
            'device_sn': 'bd2_003',
            # 'file_name': '28M视频文件.mp4',
            'upload_id': '1623242352fbc06b8be3e10548881ad8166a500f5406f5973696dfbb8ec232ccaed7176256',
            'key': 'test/bd2_003/normal_file/28M视频文件.mp4',
            # 'part_number': 3,
            'etags': ['{"part_number": 1, "e_tag": "b39215e1c1b8063113b772bbba2558fe"}',
                      '{"part_number": 2, "e_tag": "2960bb38c84243bd9dd05f05b722e268"}',
                      '{"part_number": 3, "e_tag": "35c2b3b999835fd2581a7a1167824eb3"}']}
    inputs = {
        "host": env['host']['tsp_ex'],
        "path": "/api/1/phoenix/upload/mutli_upload_complete",
        "method": "POST",
        "params": {
            "app_id": app_id,
            "sign": ""
        },
        "data": data,
        "files": {"file": ""},
    }
    response = hreq.request(env, inputs)
    logger.debug(f"response {response}")
    assert response['result_code'] == 'success'
