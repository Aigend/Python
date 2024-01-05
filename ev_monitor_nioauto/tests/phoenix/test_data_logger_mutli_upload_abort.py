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


def test_get_multi_list_part(env):
    # http://showdoc.nevint.com/index.php?s=/44&page_id=19756
    """
     "upload_id": "162320886970992fbf7a7a3232683b6be15c42bab08066ce4581e7d932feb0663b62008318",
    "key": "test/bd2_003/normal_file/test_upload.mp4"

    """
    app_id = 100466
    host = "https://media-test.nioint.com"
    inputs = {
        "host": host,
        "path": "/api/1/in/cos/file/multi_list_part",
        "method": "GET",
        # "headers": headers_from_data,
        "params": {
            "app_id": app_id,
            "upload_id": "162320886970992fbf7a7a3232683b6be15c42bab08066ce4581e7d932feb0663b62008318",
            "key": "test/bd2_003/normal_file/test_upload.mp4",
            "sign": ""
        }
    }
    response = hreq.request(env, inputs)
    logger.debug(f"response {response}")
    assert response['result_code'] == 'success'


def test_data_logger_mutli_upload_abort(env, mysql):
    """
    查询状态接口
        http://showdoc.nevint.com/index.php?s=/44&page_id=19756

        https://nio.feishu.cn/docs/doccngR24LsBEUXNm6tV3kDbSeg#
        "upload_id": "162320798448e918b11e1a208b91cb7169afb6e932c0596bd9fd1dfa06d49c4f3f5d0bb640",
    "key": "test/bd2_003/normal_file/test_upload.mp4"

    """

    app_id = 100466
    data = {
        "device_token": "10f5767b-f879-4410-bb57-606c531d6c6b",
        "device_sn": "bd2_003",
        "upload_id": "162320886970992fbf7a7a3232683b6be15c42bab08066ce4581e7d932feb0663b62008318",
        "key": "test/bd2_003/normal_file/test_upload.mp4",
    }
    encode_data = encode_multipart_formdata(data)
    format_data = encode_data[0]
    headers_from_data = {"content-type": encode_data[1]}
    inputs = {
        "host": env['host']['tsp_ex'],
        "path": "/api/1/phoenix/upload/mutli_upload_abort",
        "method": "POST",
        "headers": headers_from_data,
        "params": {
            "app_id": app_id,
            "sign": ""
        },
        "data": format_data,
    }
    response = hreq.request(env, inputs)
    logger.debug(f"response {response}")
    assert response['result_code'] == 'success'
