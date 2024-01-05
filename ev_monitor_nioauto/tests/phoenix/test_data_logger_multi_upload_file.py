# -*- coding: utf-8 -*-
# coding:unicode_escape
# @Project : ev_monitor_nioauto
# @File : test_datalogger_status_report.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/3 11:15 上午
# @Description :


import time
import json
import os
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from urllib3 import encode_multipart_formdata


def multi_upload_init(env):
    """
    res = {
        "data": {
            "upload_id": "162313795846f90b5cbd03ce5a82f33c16c0bc3e0be5b5f9c917f33bc130b236919f7de0f1",
            "key": "test/bd2_003/normal_file/test_upload.mp4"
        },
        "request_id": "mk-rBkMNmC_HqYBRQADVvo",
        "result_code": "success",
        "server_time": 1623137958
    }
    """
    app_id = 100466
    data = {
        "device_token": "10f5767b-f879-4410-bb57-606c531d6c6b",
        "device_sn": "bd2_003",
        "file_name": "test_upload.mp4",
    }
    encode_data = encode_multipart_formdata(data)
    format_data = encode_data[0]
    headers_from_data = {"content-type": encode_data[1]}
    inputs = {
        "host": env['host']['tsp_ex'],
        "path": "/api/1/phoenix/upload/mutli_upload_init",
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
    data["upload_id"] = response["data"]["upload_id"]
    data["key"] = response["data"]["key"]
    return data


def test_data_logger_multi_upload_file(env, mysql):
    """
        https://nio.feishu.cn/docs/doccngR24LsBEUXNm6tV3kDbSeg#
        device_token
        device_sn
        upload_id
        key
        part_number
    """
    ls = [{
        "part_number": 1,
        "e_tag": "b39215e1c1b8063113b772bbba2558fe"
    }, {
        "part_number": 2,
        "e_tag": "2960bb38c84243bd9dd05f05b722e268"
    }, {
        "part_number": 3,
        "e_tag": "35c2b3b999835fd2581a7a1167824eb3"
    }
    ]

    data = multi_upload_init(env)

    file_dir = "./data"
    file_msg = {}
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_msg[str(file).split("_")[-1].split('.')[0]] = f"{file_dir}/{file}"
    logger.debug(file_msg)
    res_list = []
    for i in range(len(file_msg)):
        part_number = i + 1
        key = '%04d' % part_number
        file_path = file_msg[key]
        logger.debug(file_path)
        app_id = 100466
        with open(file_path, mode="rb") as f:  # 打开文件
            data['file'] = (key, f.read())
        data['part_number'] = part_number
        encode_data = encode_multipart_formdata(data)
        format_data = encode_data[0]
        headers = {"content-type": encode_data[1]}
        inputs = {
            "host": env['host']['tsp_ex'],
            "path": "/api/1/phoenix/upload/multi_upload_file",
            "method": "POST",
            "headers": headers,
            "params": {
                "app_id": app_id,
                "sign": ""
            },
            "data": format_data,
        }
        response = hreq.request(env, inputs)
        logger.debug(f"response {response}")
        res_list.append(response['data'])
    logger.debug(res_list)

def mutli_upload_complete(env, mysql):
    """
        https://nio.feishu.cn/docs/doccngR24LsBEUXNm6tV3kDbSeg#
        device_token
        device_sn
        upload_id
        key
        etags

    """

    app_id = 100466
    device_token = "10f5767b-f879-4410-bb57-606c531d6c6b"
    device_sn = "bd2_003"
    upload_id = ""
    key = ""
    etags = []
    data = {
        "device_token": device_token,
        "device_sn": device_sn,
        "upload_id": upload_id,
        "key": key,
        "etags": etags,
    }
    encode_data = encode_multipart_formdata(data)
    format_data = encode_data[0]
    headers_from_data = {"content-type": encode_data[1]}
    inputs = {
        "host": env['host']['tsp_ex'],
        "path": "/api/1/phoenix/upload/mutli_upload_complete",
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
