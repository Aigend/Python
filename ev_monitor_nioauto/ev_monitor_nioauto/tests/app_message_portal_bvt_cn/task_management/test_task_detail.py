# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_task_detail.py
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
from utils.message_formator import format_to_task_detail

cancel_task_path = "/api/2/in/message_portal/task/detail"
server_app_id = 10000


@pytest.mark.parametrize("case_name,res_app_id", [
    ("正案例_获取自己服务app_id的任务详情", "10000"),
])
def test_task_detail(env, mysql, case_name, res_app_id):
    mysql_result = mysql['nmp_app'].fetch("message_task", {"id>": 0, "app_id": res_app_id}, suffix="limit 5")
    task_id_list = [str(res.get("id")) for res in mysql_result]
    task_ids = ",".join(task_id_list)
    logger.debug(f"任务ID：{task_ids}")
    with allure.step(f'取消发送任务接口{cancel_task_path}'):
        http = {
            "host": env['host']['app_in'],
            "path": cancel_task_path,
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "ids": str(task_ids),
                "app_id": server_app_id,
                "sign": ""}
        }
        response = hreq.request(env, http)
        assert response.get("result_code") == "success"
        mysql_result = mysql['nmp_app'].fetch("message_task", {"id in": task_id_list, "app_id": server_app_id},retry_num=5)
        assert len(mysql_result) == len(response["data"])
