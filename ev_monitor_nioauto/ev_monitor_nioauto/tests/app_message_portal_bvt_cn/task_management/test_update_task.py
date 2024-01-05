# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_update_task.py
# @Author : qiangwei.zhang
# @time: 2021/08/09
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import pytest
import allure
import time
import json

from tests.app_message_portal.template_management.template_server import create_new_template, get_published_template_id
from utils.http_client import TSPRequest as hreq
from utils.random_tool import int_time_to_format_time, format_time
from tests.app_message_portal.task_management.task_server import create_task, generate_task_detail

update_task_path = "/api/2/in/message_portal/task/update"


def test_update_task(env, cmdopt, mysql):
    task_id = create_task(env, mysql)
    recipients = "550736273@qq.com,842244250@qq.com"
    send_time = int(time.time()) + 5 * 60 * 60
    service_type = "cn" if cmdopt in ["test", "stg"] else "eu"
    with allure.step(f'更新发送任务接口'):
        push_type = "email"
        template_name = "L_R_no_repeat"
        task_detail = generate_task_detail(env, mysql, push_type, service_type, template_name, "recipients", recipients)
        app_id = 10000
        json_content = {
            "id": task_id,
            "execution_data": json.dumps(task_detail),
            "appointment_time": send_time,
        }
        http = {
            "host": env['host']['app_in'],
            "path": update_task_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": json_content
        }
        response = hreq.request(env, http)
        assert response.get("result_code") == "success"


@pytest.mark.parametrize("case_name,app_id,id_type,channel", [
    ("正案例_更新为已发布的模板", "10000", "published", "email"),
])
def test_update_task_by_template_status(env, mysql, cmdopt, case_name, app_id, id_type, channel):
    task_id = create_task(env, mysql)
    template_id = get_published_template_id(env, mysql)
    with allure.step('创建任务接口'):
        recipients = "550736273@qq.com,842244250@qq.com"
        send_time = int(time.time()) + 5 * 60 * 60
        service_type = "cn" if cmdopt in ["test", "stg"] else "eu"
        with allure.step(f'更新发送任务接口'):
            push_type = "email"
            template_name = "L_R_no_repeat"
            if template_id and template_id != "-1":
                task_detail = generate_task_detail(env, mysql, push_type, service_type, template_name, "recipients", recipients, template_id=template_id)
            else:
                task_detail = {
                    'push_type': 'email',
                    'service_type': 'cn',
                    'push_data': {
                        'recipients': '550736273@qq.com,842244250@qq.com',
                        'template_id': template_id,
                        'replace_values': [
                            {'id': '550736273@qq.com', 'replace_map': {'date': 'QA_RS_CCRdaXXTnw', 'fist_name': 'QA_RS_UNONUJcqry'}},
                            {'id': '842244250@qq.com', 'replace_map': {'date': 'QA_RS_MefsplbGOC', 'fist_name': 'QA_RS_RGORZtkLDe'}}]
                    }
                }

            app_id = 10000
            json_content = {
                "id": task_id,
                "execution_data": json.dumps(task_detail),
                "appointment_time": send_time,
            }
            http = {
                "host": env['host']['app_in'],
                "path": update_task_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_content
            }
            response = hreq.request(env, http)
            if "正案例" in case_name:
                assert response.get("result_code") == "success"
            else:
                assert response.get("result_code") == "invalid_param"
