# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_create_task.py
# @Author : qiangwei.zhang
# @time: 2021/08/09
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import pytest
import time
import json

from utils.http_client import TSPRequest as hreq
from tests.app_message_portal.template_management.template_server import init_email_template, get_template_detail
from tests.app_message_portal.task_management.task_server import create_task, generate_task_detail

create_task_path = "/api/2/in/message_portal/task/create"
server_app_id = 10000
recipients_map = {
    "cn": "550736273@qq.com,842244250@qq.com",
    "eu": "550736273@qq.com,842244250@qq.com",
    "employee": "qiangwei.zhang@nio.com,qiangwei.zhang.o@nio.com",
}


class TestCreateTask(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_email_template(env, mysql)

    create_task_keys = "case_name,send_time,channel,template_name"
    create_task_cases = [
        ("正案例_任务时间测试_当前时间,其他不为空", int(time.time()), "email", "no_variable"),
        ("正案例_任务时间测试_当前时间，send_time为None", None, "email", "L_R_no_repeat"),
        ("正案例_任务时间测试_当前时间,channel为None", int(time.time()), None, "L_R_no_repeat"),
        ("正案例_任务时间测试_当前时间,send_time为None，channel为None", None, None, "L_R_no_repeat"),
        ("正案例_任务时间测试_1小时后", int(time.time()) + 60 * 60, "email", "L_R_no_repeat"),
    ]
    create_task_ids = [f"{case[0]}" for case in create_task_cases]

    @pytest.mark.parametrize(create_task_keys, create_task_cases, ids=create_task_ids)
    def test_create_task(self, env, cmdopt, mysql, case_name, send_time, channel, template_name, prepare_template):

        region_list = ["cn", "employee"]
        if "marcopolo" in cmdopt:
            region_list = ["eu", "employee"]
        for region in region_list:
            recipients = recipients_map.get(region)
            user_keys = "recipients"
            with allure.step(f'创建发送任务接口'):
                push_type = "email"
                service_type = region
                task_detail = generate_task_detail(env, mysql, push_type, service_type, template_name, user_keys, recipients)
                json_content = {
                    "execution_data": json.dumps(task_detail),
                    "appointment_time": send_time,
                }
                if not json_content.get("appointment_time"):
                    json_content.pop("appointment_time")
                inputs = {
                    "host": env['host']['app_in'],
                    "path": create_task_path,
                    "method": "POST",
                    "headers": {"Content-Type": "application/json"},
                    "params": {"region": region, "lang": "zh-cn", "hash_type": "sha256", "app_id": 10000, "sign": ""},
                    "json": json_content
                }
                response = hreq.request(env, inputs)
                assert response.get("result_code") == "success"
                task_id = response.get("data")
            with allure.step(f'校验mysql中状态改为0'):
                mysql_result = mysql['nmp_app'].fetch("message_task", {"id": task_id})
                assert len(mysql_result) == 1
        # with allure.step(f'清除测试数据'):
        #     if 'test' in cmdopt:
        #         mysql['nmp_app'].delete("message_task", {"id": task_id})
