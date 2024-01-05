# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_cancel_task.py
# @Author : qiangwei.zhang
# @time: 2021/08/09
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import pytest
import time
import json
from utils.random_tool import random_string
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.random_tool import int_time_to_format_time, format_time
from tests.app_message_portal.task_management.task_server import create_task

cancel_task_path = "/api/2/in/message_portal/task/cancel"


def test_cancel_task(env, mysql, ):
    task_id = create_task(env, mysql)
    logger.debug(f"任务ID：{task_id}")
    with allure.step(f'取消发送任务接口{cancel_task_path}'):
        app_id = 10000
        http = {
            "host": env['host']['app_in'],
            "path": cancel_task_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {"id": task_id}
        }
        response = hreq.request(env, http)
        assert response.get("result_code") == "success"
    with allure.step(f'校验mysql中状态改为0'):
        mysql_result = mysql['nmp_app'].fetch("message_task", {"id": task_id})
        assert mysql_result[0].get("status") == 0
    with allure.step(f'清除测试数据'):
        mysql['nmp_app'].delete("message_task", {"id": task_id})
