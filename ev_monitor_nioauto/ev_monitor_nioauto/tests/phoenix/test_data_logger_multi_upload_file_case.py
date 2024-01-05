# -*- coding: utf-8 -*-
# coding:unicode_escape
# @Project : ev_monitor_nioauto
# @File : test_datalogger_status_report.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/3 11:15 上午
# @Description :
import hashlib
import time
import allure
import os
import json

import pytest

from config.settings import BASE_DIR
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.file_split_by_size import split
from utils.random_tool import int_time_to_format_time

"""

208558	LJ1E6A2U7K5302252	02832f518d6f31b2e4bbc1fae385cd20	27	prod/phoenix_datalogger/dl01_015/allmessages_2022-03-14_08-47-06_2022-03-14_08-50-17_27.mf4	2	1		2022-03-14 01:52:36	2022-03-14 19:56:53	{"vin":"LJ1E6A2U7K5302252","uuid":"02832f518d6f31b2e4bbc1fae385cd20","index":27,"model_type":"ES6","model_type_year":"G1.3","f141":"ES6.G1.1.AU.01*3.1.2build2","dbc_version":"ES6_3.0.11"}
208557	LJ1EFAUU7NG000031	d42c33f691e4419d2edc560d792a2b79	18	prod/phoenix_datalogger/dl02_025/allmessages_2022-03-14_09-49-09_2022-03-14_09-51-15_18.mf4	2	1		2022-03-14 01:52:33	2022-03-14 23:09:33	{"vin":"LJ1EFAUU7NG000031","uuid":"d42c33f691e4419d2edc560d792a2b79","index":18,"model_type":"ET7","model_type_year":"G1.1","f141":"ET7.G1.1.AG.01*0.7.0build1","dbc_version":"ET7_v00.03.00_00"}
208556	LJ1E6A3U9K5302042	b362b893f074e60bbea823081a77ca53	17	prod/phoenix_datalogger/dl01_014/allmessages_2022-03-14_09-45-18_2022-03-14_09-48-49_17.mf4	2	1		2022-03-14 01:52:22	2022-03-14 20:43:13	{"vin":"LJ1E6A3U9K5302042","uuid":"b362b893f074e60bbea823081a77ca53","index":17,"model_type":"ES8","model_type_year":"G1.F","f141":"ES8.G1.1.F.AB.01*3.1.2build2","dbc_version":"ES8_3.0.11"}
208555	LJ1E6A3U9K5302042	b362b893f074e60bbea823081a77ca53	16	prod/phoenix_datalogger/dl01_014/allmessages_2022-03-14_09-41-47_2022-03-14_09-45-18_16.mf4	2	1		2022-03-14 01:51:49	2022-03-14 21:16:28	{"vin":"LJ1E6A3U9K5302042","uuid":"b362b893f074e60bbea823081a77ca53","index":16,"model_type":"ES8","model_type_year":"G1.F","f141":"ES8.G1.1.F.AB.01*3.1.2build2","dbc_version":"ES8_3.0.11"}
"""


# @pytest.fixture(scope='function', autouse=False)
# def prepare(cmdopt):
#     file_path = os.sep.join([BASE_DIR, 'data', "phoenix", 'allmessages_2022-03-30_14-36-19_2022-03-30_14-38-23_1.mf4'])
#     to_dir = os.sep.join([BASE_DIR, 'data', "phoenix", 'data'])
#     file_size = os.path.getsize(file_path)
#     file_name = os.path.basename(file_path)
#     file_type = "日志文件"
#     file_msg = split(file_path, to_dir, file_size=10, file_name="new_data", suffix=".mf4")
#     request_data = {
#         "file_path": file_path,
#         "vin": "LJ1EFAUU7NG000031",
#         "device_type": "datalogger",
#         "file_size": file_size,
#         "file_name": file_name,
#         "file_type": file_type,
#         "file_msg": file_msg,
#     }
#     if cmdopt == "stg":
#         request_data["device_token"] = "bd78fca4-eee6-4d0e-af25-d76aaebbcdcb"
#         request_data["device_sn"] = "pressure_010"
#     elif cmdopt == "test":
#         request_data["device_token"] = "b11b42ce-94e3-4416-a9e1-65ca264d7469"
#         request_data["device_sn"] = "dl01_004"
#     return request_data


@pytest.mark.parametrize("vin,filename,model_type,index", (
        # ["LJ1E6A2U7K5302252", "allmessages_2022-03-14_08-47-06_2022-03-14_08-50-17_27.mf4", "ES6", 1],
        # ["LJ1EFAUU7NG000031", "allmessages_2022-06-14_09-49-21_2022-06-14_09-51-13_361.mf4", "ET7", 1],
        # ["LJ1E6A3U9K5302042", "allmessages_2022-03-14_09-45-18_2022-03-14_09-48-49_17.mf4", "ES8", 1],
        # ["LJ1E6A2U7K5302252", "LJ1E6A2U7K5302252_ES6_0614_12.mf4", "ES6",1],
        # ["LJ1E6A2U7K5302252", "allmessages_2022-06-14_13-33-28_2022-06-14_13-34-35_1.mf4", "ES6", 1],
        # ["LJ1E6A2U7K5302252", "allmessages_2022-06-14_13-34-35_2022-06-14_13-37-57_2.mf4", "ES6", 2],
        # ["LJ1E6A2U7K5302252", "allmessages_2022-06-14_13-37-57_2022-06-14_13-41-18_3.mf4", "ES6", 3],
        # ["LJ1E6A2U7K5302252", "allmessages_2022-06-14_13-41-18_2022-06-14_13-45-23_4.mf4", "ES6", 4],
        # ["LJ1E6A2U7K5302252", "allmessages_2022-06-14_13-45-23_2022-06-14_13-48-40_5.mf4", "ES6", 5],
        # ["LJ1EFAUU7NG000031", "LJ1EFAUU7NG000031_ET7_0614_361.mf4", "ET7", 1],
        # ["LJ1E6A3U9K5302042", "LJ1E6A3U9K5302042_ES8_0614_1.mf4", "ES8", 1],
        # ["LJ1E6A2U7K7704356", "allmessages_2022-06-09_11-52-45_2022-06-09_11-54-51_67.mf4", "ES6", 1],
        # ["SQETEST0143121814", "allmessages_2022-03-14_09-45-18_2022-03-14_09-48-49_17.mf4", "ES8", 1],  # eu
        ['LJ1E6A2U7K5302252', 'allmessages_2022-06-23_10-18-34_2022-06-23_10-21-50_1.mf4', 'ES6', 1],
        ['LJ1E6A2U7K5302252', 'allmessages_2022-06-23_10-21-50_2022-06-23_10-27-30_2.mf4', 'ES6', 2],
        ['LJ1E6A2U7K5302252', 'allmessages_2022-06-23_10-27-30_2022-06-23_10-38-20_3.mf4', 'ES6', 3],
        ['LJ1E6A2U7K5302252', 'allmessages_2022-06-23_10-38-20_2022-06-23_10-48-43_4.mf4', 'ES6', 4],
        ['LJ1E6A2U7K5302252', 'allmessages_2022-06-23_10-48-43_2022-06-23_10-58-17_5.mf4', 'ES6', 5],
        ['LJ1E6A2U7K5302252', 'allmessages_2022-06-23_10-58-17_2022-06-23_11-01-33_6.mf4', 'ES6', 6],
        ['LJ1E6A2U7K5302252', 'allmessages_2022-06-23_11-01-33_2022-06-23_11-04-30_7.mf4', 'ES6', 7],

))
def test_multi_upload_file(env, cmdopt, vin, filename, model_type, index):
    file_path = os.sep.join([BASE_DIR, 'data', "phoenix", filename])
    to_dir = os.sep.join([BASE_DIR, 'data', "phoenix", 'data'])
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    file_type = "日志文件"
    file_msg = split(file_path, to_dir, file_size=10, file_name="new_data", suffix=".mf4")
    prepare = {
        "file_path": file_path,
        "vin": vin,
        "device_type": "datalogger",
        "file_size": file_size,
        "file_name": file_name,
        "file_type": file_type,
        "file_msg": file_msg,
    }
    if cmdopt == "stg":
        prepare["device_token"] = "bd78fca4-eee6-4d0e-af25-d76aaebbcdcb"
        prepare["device_sn"] = "pressure_010"
    elif cmdopt == "test":
        prepare["device_token"] = "b11b42ce-94e3-4416-a9e1-65ca264d7469"
        prepare["device_sn"] = "dl01_004"

    execute_times = 1  # 上传文件执行次数

    app_id = 100466
    host = env["host"]["phoenix_ex"]
    for i in range(execute_times):
        data = {
            "device_token": prepare.get("device_token"),
            "device_sn": prepare.get("device_sn"),
            "file_name": prepare.get("file_name"),
        }
        with allure.step("多文件上传初始化接口"):
            inputs = {
                "host": host,
                "path": "/api/1/phoenix/upload/mutli_upload_init",
                "method": "POST",
                "params": {
                    "app_id": app_id,
                    "sign": ""
                },
                "data": data,
            }
            response = hreq.request(env, inputs)
            logger.debug(f"response {response}")
            data["upload_id"] = response["data"]["upload_id"]
            data["key"] = response["data"]["key"]
        with allure.step("多文件上传接口"):
            file_msg = prepare.get("file_msg")
            res_list = []
            for i in range(len(file_msg)):
                part_number = i + 1
                key = "%04d" % part_number
                split_file_path = file_msg[key]
                logger.debug(split_file_path)
                data["part_number"] = part_number
                inputs = {
                    "host": host,
                    "path": "/api/1/phoenix/upload/multi_upload_file",
                    "method": "POST",
                    "params": {
                        "app_id": app_id,
                        "sign": ""
                    },
                    "data": data,
                    "files": {"file": open(split_file_path, "rb")},
                }
                response = hreq.request(env, inputs)
                logger.debug(f"response {response}")
                res_list.append(response["data"])
            logger.debug(res_list)
            data.pop("file_name")
            data.pop("part_number")
            data["etags"] = json.dumps(res_list)
        with allure.step("多文件上传完成接口"):
            inputs = {
                "host": host,
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
            assert response["result_code"] == "success"
            remote_path = response.get("data")
        with allure.step("多文件上传成功通知接口"):
            extend_info = {
                "msg": "测试使用extend_info",
            }
            inputs = {
                "host": host,
                "path": "/api/1/phoenix/upload/file_upload_notice",
                "method": "POST",
                "headers": {"content-type": "application/json"},
                "params": {
                    "app_id": app_id,
                    "sign": ""
                },
                "json": {
                    "device_token": prepare.get("device_token"),
                    "device_type": prepare.get("device_type"),
                    "device_sn": prepare.get("device_sn"),
                    "file_type": prepare.get("file_type"),
                    "file_name": prepare.get("file_name"),
                    "file_size": prepare.get("file_size"),
                    "remote_path": remote_path,
                    "start_time": int(time.time()) - 360,
                    "end_time": int(time.time()),
                    "extend_info": json.dumps(extend_info),
                }
            }
            response = hreq.request(env, inputs)
            logger.debug(f"response {response}")
            assert response["result_code"] == "success"
        with allure.step("文件分组"):
            vin = prepare.get("vin")
            sn = prepare.get("device_sn")
            event_type = "mdf_upload"
            start_time = int_time_to_format_time(int(time.time()) - 60 * 30)
            end_time = int_time_to_format_time()
            sig_param = f"{vin}{sn}{event_type}{start_time}"
            uuid = hashlib.md5(sig_param.encode('utf-8')).hexdigest()
            inputs = {
                "host": host,
                "path": "/api/1/phoenix/datalogger/upload_group",
                "method": "POST",
                "headers": {"content-type": "application/x-www-form-urlencoded"},
                "params": {
                    "app_id": app_id,
                    "sign": ""
                },
                "data": {
                    "device_sn": prepare.get("device_sn"),
                    "device_token": prepare.get("device_token"),
                    "event_type": event_type,
                    "vin": vin,
                    "device_type": "bd2",
                    "file_type": "mdf",
                    "uuid": uuid,
                    "signal_start_time": int(time.time() * 1000) - 30 * 24 * 60 * 60 * 1000,
                    "signal_end_time": int(time.time() * 1000),
                    "start_time": start_time,
                    "end_time": end_time,
                    "path": remote_path,
                    "index": index,
                    "total": len(file_msg)
                }
            }
            response = hreq.request(env, inputs)
            logger.debug(f"response {response}")
            assert response["result_code"] == "success"
