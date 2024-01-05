# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_syslog_upload.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/7/6 2:27 下午
# @Description :

"""
业务过程：
数据准备：
    1.日志文件：日期，条数
    2.车辆：在线（用于下发命令）
    3.did版本，status_did实时版本信息（上线早），log_did_data变化版本信息（上线晚），理论上log_did_data中的最新版本号和status_did中一致；
        除非是很久未更新的车辆会有版本号只存在status_did表中
1.定时任务触发,页面修改或者修改schedule_config表time字段
2.掉接口上传日志到S3（"/api/1/data/vehicle/{vid}/logs"）
    接口返回 S3_path
3.查看日志命令下发记录，
    查到对应车辆本次下发的command_id，diagnosis_syslog_upload表
4.将S3日志文件路径写入rvs指令下发结果中，并将数据状态改为0成功
    control_online_commmand表，id即为command_id
    {"file_info":{"file_paths":["S3_path"]}}
4.修改phonix库中对应状态为status=2(3:失败;2:下发中;1:成功)，to_es=1（3:失败;2:已发送;1：未发送）
5.等候定时任务执行：状态变为status=1，to_es=2
6.查询search中解析到的结果

1.log_did_data有全部版本信息✅
2.log_did_data无版本，status_did无版本✅
3.status_did有全部版本,log_did_data无匹配版本✅
4.日志包含多天，log_did_data版本包含多个日期版本✅

问题1：status_did表ecu版本采样时间需要小于日志时间么
问题2：一部分版本信息在status_did表，一部分版本信息在log_did_data表，会全部匹配么
问题3：日志与ecu版本的匹配是每条日志都会进行一次匹配么，还是同一个时间批次的匹配一次

"""

"""
INSERT INTO `log_did_data` (`id`, `vid`, `tag`, `ecu`, `did_id`, `value`, `sample_time`, `update_time`, `previous_value`)
VALUES
	( '92dfb6d9b79641b5823c6fc1c3109764', 'did_tag1625642216', 'ADC', 'F110', 'P2234091 AD', '2021-06-24 07:16:56.327', '2021-06-24 07:16:56.32', NULL),
	('92dfb6d9b79641b5823c6fc1c3109764', 'did_tag1625642216', 'ADC', 'F118', 'P2234092 AD', '2021-06-24 07:16:56.327', '2021-06-24 07:16:56.327', NULL),
	('92dfb6d9b79641b5823c6fc1c3109764', 'did_tag1625642216', 'CDC', 'F110', 'P1234261 AD', '2021-06-24 07:16:56.327', '2021-06-24 07:16:56.327', NULL),
	('92dfb6d9b79641b5823c6fc1c3109764', 'did_tag1625642216', 'CDC', 'F118', 'P1234142 AD', '2021-06-24 07:16:56.327', '2021-06-24 07:35:57.693', NULL),
	('92dfb6d9b79641b5823c6fc1c3109764', 'did_tag1625642216', 'CDC', 'F18C', 'P1234143 AA', '2021-06-24 07:16:56.327', '2021-06-24 07:36:15.914', NULL),
	('92dfb6d9b79641b5823c6fc1c3109764', 'did_tag1625642216', 'CGW', 'F110', 'P2234331 AD', '2021-06-24 07:16:56.327', '2021-06-24 07:16:56.327', NULL),
	('92dfb6d9b79641b5823c6fc1c3109764', 'did_tag1625642216', 'CGW', 'F118', 'P2234332 AD', '2021-06-24 07:16:56.327', '2021-06-24 07:16:56.327', NULL),
	('92dfb6d9b79641b5823c6fc1c3109764', 'did_tag1625642216', 'CGW', 'F141', 'P2234333 AA', '2021-06-24 07:16:56.327', '2021-06-24 02:49:31.949', NULL);
"""

import time
import pytest
import os
import allure
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.random_tool import int_time_to_format_time, format_date_n_hours_ago, time_sleep
from urllib3 import encode_multipart_formdata
import requests

file_path_magneto_log1 = "../../data/file_upload_data/syslog/5B6CB7743A7C78034750E3A76B121DB0_magneto.log.1.gz"
file_path_magneto_log2 = "../../data/file_upload_data/syslog/5BCACACA783A206A9B72AFAE921668DF_magneto.log.0.gz"
file_path_magneto_log3 = "../../data/file_upload_data/syslog/5D9F2C81B29AB84D1BE7B638F6FE0C27_magneto.log.0.gz"
file_path_sys_log1 = "../../data/file_upload_data/syslog/6BB141F9296308C96A038B2C16826495_syslog.6.gz"
file_path_sys_log2 = "../../data/file_upload_data/syslog/6F5432C58B1D6F4103BEEA1ABBB3DA0E_syslog.1.gz"
file_path_sys_log3 = "../../data/file_upload_data/syslog/691009A0878D1FA1A6FE6DDFA264229B_syslog.0.gz"
file_path_sys_log4 = "../../data/file_upload_data/syslog/test_syslog.1.gz"
file_path_sys_log5 = "../../data/file_upload_data/syslog/A2F8B64196057744DEACE233BCA43F56_syslog.7.gz"


@pytest.mark.parametrize('file_path, vid, vin, command_id', [
    (file_path_magneto_log2, '92dfb6d9b79641b5823c6fc1c3109764', "SQETEST0552256477", 1466384),
    # (file_path_sys_log1, '92dfb6d9b79641b5823c6fc1c3109764', "SQETEST0552256477", 1466384),
    # (file_path_sys_log5, '4fce80aa8c0f4d59a8209e1974e33e4d', "SQETEST0407885840", 1469083),
    # (file_path_sys_log1, '4fce80aa8c0f4d59a8209e1974e33e4d', "SQETEST0407885840", 1469083),
])
def test_sys_logger_upload_file(env, mysql, file_path, vid, vin, command_id):
    with allure.step("日志上传接口"):
        app_id = 100240
        inputs = {
            "host": env['host']['tsp_ex'],
            "path": f"/api/1/data/vehicle/{vid}/logs",
            "method": "POST",
            "params": {
                "app_id": app_id,
                "lang": "zh-cn",
                "type": "sys_log",
                "sign": "",
            },
            "data": {"command_id": command_id, },
            "files": {"file": open(file_path, "rb")},
        }
        response = hreq.request(env, inputs)
        logger.debug(f"response {response}")
        assert response['result_code'] == 'success'
        remote_path = response.get("data")


def test_upload_syslog(mysql, env, ):
    vin = "SQETEST0552256477"
    vid = "92dfb6d9b79641b5823c6fc1c3109764"
    file_path = file_path_sys_log1
    second = 70
    int_time = int(time.time()) + second
    format_time = int_time_to_format_time(int_time)
    hm = format_time[11:16]
    logger.debug(f"定时任务执行时间{hm}")
    format_time_new = format_time[:-2] + '00'
    mysql_time = format_date_n_hours_ago(format_time_new, 8)
    logger.debug(f"数据库创建记录时间{mysql_time}")
    mysql['phoenix'].update("schedule_config", {"id": 1, 'type': "syslog_upload"}, {"time": hm})
    time_sleep(second + 5)
    # time.sleep(second + 5)
    record_in_mysql = mysql['phoenix'].fetch("diagnosis_syslog_upload", {'vin': vin, 'log_type': "sys_log", "create_time": mysql_time})
    logger.debug(record_in_mysql)
    command_id = record_in_mysql[0]['command_id']
    phoenix_record_id = record_in_mysql[0]['id']
    app_id = 100240
    inputs = {
        "host": env['host']['tsp_ex'],
        "path": f"/api/1/data/vehicle/{vid}/logs",
        "method": "POST",
        "params": {
            "app_id": app_id,
            "lang": "zh-cn",
            "type": "sys_log",
            "command_id": command_id,
            "sign": "",
        },
        "files": {"file": open(file_path, "rb")},
    }
    response = hreq.request(env, inputs)
    logger.debug(f"response {response}")
    assert response['result_code'] == 'success'
    remote_path = response.get("data").get("log_path")
    file_info = {"file_info": {"file_paths": [remote_path]}}
    mysql['rvs'].update("control_online_commmand", {"id": command_id}, {"result_params": str(file_info), "status": 0})
    time.sleep(5)
    record_in_mysql_2 = mysql['phoenix'].fetch("diagnosis_syslog_upload", {'id': phoenix_record_id})
    status = record_in_mysql_2[0]['status']
    to_es = record_in_mysql_2[0]['to_es']
    if status == 3 and to_es == 3:
        mysql['phoenix'].update("diagnosis_syslog_upload", {"id": phoenix_record_id}, {'status': 2, "to_es": 1})
    record_in_mysql_3 = mysql['phoenix'].fetch("diagnosis_syslog_upload", {'id': phoenix_record_id, 'status': 1, "to_es": 2}, retry_num=70)
    assert len(record_in_mysql_3) == 1
