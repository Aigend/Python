# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : task_server.py
# @Author : qiangwei.zhang
# @time: 2021/08/09
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import time
import string
import json
import random
from utils.http_client import TSPRequest as hreq
from utils.random_tool import int_time_to_format_time, format_time
from tests.app_message_portal.template_management.template_server import init_email_template, init_sms_template, init_app_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import generate_private_variable_replace, extracted_private_variable_from_template

create_task_path = "/api/2/in/message_portal/task/create"
app_id = 10000


def create_task(env, mysql, push_type="email", service_type="eu", template_name="L_R_no_repeat", user_keys="recipients", user_values="842244250@qq.com,550736273@qq.com",
                send_time=int(time.time()) + 60 * 60):
    task_detail = generate_task_detail(env, mysql, push_type, service_type, template_name, user_keys, user_values)
    json_content = {
        "execution_data": json.dumps(task_detail),
        "appointment_time": send_time,
    }
    http = {
        "host": env['host']['app_in'],
        "path": create_task_path,
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
        "json": json_content
    }
    response = hreq.request(env, http)
    if response.get("result_code") == "success":
        return response.get("data")
    else:
        return response


def generate_task_detail(env, mysql, push_type, service_type, template_name=None, user_keys="recipients", user_values="550736273@qq.com", snapshot=False, template_id=None):
    if not template_id:
        template_app_map = init_app_template(env, mysql)
        template_email_map = init_email_template(env, mysql)
        template_sms_map = init_sms_template(env, mysql)
        template_id_map = {**template_app_map, **template_email_map, **template_sms_map}
        template_id = template_id_map.get(template_name)
    template_version = ''
    if snapshot:
        template_snapshot = mysql["nmp_app"].fetch("message_template_snapshot", {"template_id": template_id}, suffix="order by create_time")
        template_content = bytes.decode(template_snapshot[0].get("template"))
        template_version = template_snapshot[0].get("version")
    else:
        template = mysql["nmp_app"].fetch("message_template", {"template_id": template_id})
        template_content = bytes.decode(template[0].get("template"))
    generate_replace_values = []
    if user_keys in ["user_ids", "account_ids", "recipients"]:
        private_variable = extracted_private_variable_from_template(template_content)
        generate_replace_values = generate_private_variable_replace(user_values, private_variable)
    task_detail = {
        "push_type": push_type,
        "service_type": service_type,
        "push_data": {
            user_keys: user_values,
            "template_id": template_id,
            "replace_values": generate_replace_values,
            "template_content": template_content,
            "snapshot": snapshot,
        }
    }
    if snapshot:
        task_detail['push_data']['version'] = template_version
    return task_detail
