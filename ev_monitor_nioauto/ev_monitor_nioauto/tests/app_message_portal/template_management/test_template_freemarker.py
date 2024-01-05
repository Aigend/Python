# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
freemarker是模版新支持的一种类型，此处单独写一个case作为补充
"""
import json
import time

import allure
import pytest

from data.email_content import free_marker
from tests.app_message_center.clear_rate_limit import clear_rate_limit
from utils.assertions import assert_equal
from utils.http_client import TSPRequest

add_template = '/api/2/in/message_portal/template/add'
publish_template = '/api/2/in/message_portal/template/publish'
offline_template = '/api/2/in/message_portal/template/offline'
update_template = '/api/2/in/message_portal/template/update'
send_email_by_template = '/api/2/in/message_portal/template/cn/email/send'
delete_template = '/api/2/in/message_portal/template/delete'
template_list = '/api/2/in/message_portal/template/list'
app_id = 10000


@pytest.fixture(autouse=True)
def freemarker_template_id(env, mysql):
    with allure.step('测试开始前生成模版'):
        sender = 'notification-test@nio.io' if 'marcopolo' in env['cmdopt'] else 'notification@nio.com'
        template = {'subject': f'[{env["cmdopt"]}]测试freemarker', 'content': free_marker, 'category': 'verify',
                    'sender_name': sender}
        http = {
            "host": env['host']['app_in'],
            "path": add_template,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ""
            },
            "json": {'channel': 'email', 'name': 'freemarker test', 'type': 'FTL', 'template_str': json.dumps(template)}
        }
        response = TSPRequest.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
    with allure.step('校验db'):
        template_id = response['data']
        result = mysql["nmp_app"].fetch_one("message_template", {"template_id": template_id})
        assert_equal(result['valid'], 1)
    with allure.step('确认模版已生成'):
        ts = int(time.time())
        http = {
            "host": env['host']['app_in'],
            "path": template_list,
            "method": "GET",
            "params": {
                "app_id": app_id,
                "channel": "email",
                "start_time": ts - 10,
                "end_time": ts + 10,
                "sign": ""
            }
        }
        response = TSPRequest.request(env, http)
        assert (template_id in [sub['template_id'] for sub in response['data']['page']])
    return template_id


def test_template_freemarker(env, redis, cmdopt, mysql, freemarker_template_id):
    clear_rate_limit(redis, cmdopt, 10022)
    with allure.step('发布模版'):
        http = {
            "host": env['host']['app_in'],
            "path": publish_template,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ""
            },
            "json": {'id': freemarker_template_id}
        }
        response = TSPRequest.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')

    with allure.step('替换模版内容并发送'):
        sender = 'notification-test@nio.io' if 'marcopolo' in env['cmdopt'] else 'notification@nio.com'
        path = '/api/2/in/message_portal/template/eu/email/send' if 'marcopolo' in env[
            'cmdopt'] else '/api/2/in/message_portal/template/cn/email/send'
        recipient = 'colin.li@nio.com'
        json_dict = {
            "channel": "email",
            "recipients": recipient,
            "sender_name": sender,
            "subject": f'[{env["cmdopt"]}]测试freemarker',
            "template_id": freemarker_template_id,
            "category": "verify",
            "replace_values": [{"id": recipient, "replace_map": {"msg": "Hello world", "flag": True, "salary": 60000,
                                                                 "avg": 0.688, "createDate": '20220331 123002',
                                                                 "stars": ['刘德华', '张学友', '黎明', '郭富城'],
                                                                 "cities": ['北京', '上海', '广州'], "score": 100}}]
        }
        inputs = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": json_dict
        }
        response = TSPRequest.request(env, inputs)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
        assert response['data']['details'][0]['message_id']
        assert_equal(response['data']['details'][0]['recipient'], recipient)
