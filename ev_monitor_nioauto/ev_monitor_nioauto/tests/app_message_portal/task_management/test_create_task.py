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
import os

from tests.app_message_portal.tag_management.tag_server import init_tag
from utils.assertions import assert_equal
from utils.random_tool import random_string
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.random_tool import int_time_to_format_time, format_time
from tests.app_message_portal.template_management.template_server import offline_template, update_template, delete_template, create_new_template, get_published_template_id
from tests.app_message_portal.template_management.template_server import init_email_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace
from config.settings import BASE_DIR
from tests.app_message_portal.task_management.task_server import create_task, generate_task_detail

create_task_path = "/api/2/in/message_portal/task/create"
# server_app_id = 10000
server_app_id = 100480

"""
定时任务时间维度
1.反案例_创建当前时间之前的任务
2.正案例_任务时间测试_创建当前时间的任务
3.正案例_任务时间测试_创建5分种之后的任务
4.正案例_任务时间测试_创建1小时之后的任务
5.正案例_任务时间测试_创建24小时之后的任务
6.正案例_任务时间测试_创建3天之后的任务
7.反案例_创建4天之后的任务
"""

sender_name_map = {
    "cn": "notification@nio.com",
    "eu": "notification-test@nio.io",
    "employee": "notification@nio.com",
}
recipients_map = {
    "cn": "550736273@qq.com,842244250@qq.com",
    "eu": "550736273@qq.com,842244250@qq.com",
    "employee": "qiangwei.zhang@nio.com,qiangwei.zhang.o@nio.com",
}


class TestCreateTask(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_email_template(env, mysql)

    @pytest.fixture(scope="class", autouse=False)
    def prepare_tag(self, env, mysql):
        return init_tag(env, mysql)

    @pytest.fixture(scope="class")
    def prepare_eu_email_account(self, env, cmdopt):
        cmdopt = "test_marcopolo" if cmdopt == 'test' else cmdopt
        # 消息平台test环境和test_marcopolo环境对应留资test_marcopolo环境
        file_path = f'{BASE_DIR}/config/{cmdopt}/email_account_info_{cmdopt}.txt'
        account_list = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    account_msg = {}
                    account_msg_list = line.split(',')
                    account_msg['account_id'] = account_msg_list[0]
                    account_msg['user_id'] = account_msg_list[1]
                    account_msg['recipient'] = account_msg_list[2]
                    account_msg['password'] = account_msg_list[3]
                    account_list.append(account_msg)
            return account_list
        else:
            logger.error(f"请先配置数据文件{file_path}\n数据格式：account_id,user_id,email,password,pseudo_email,create_time")

    # 100480,10000,1000075,1000045,1000154,1000109
    create_task_keys = "case_name,send_time,channel,template_name"
    create_task_cases = [
        # ("正案例_任务时间测试__5分钟前", int(time.time()) - 5 * 60, "email", "L_R_no_repeat"),
        ("正案例_任务时间测试_当前时间,其他不为空", int(time.time()), "email", "no_variable"),
        # ("正案例_任务时间测试_当前时间，send_time为None", None, "email", "L_R_no_repeat", 10000),
        # ("正案例_任务时间测试_当前时间,channel为None", int(time.time()), None, "L_R_no_repeat"),
        # ("正案例_任务时间测试_当前时间,send_time为None，channel为None", None, None, "L_R_no_repeat"),
        # ("正案例_任务时间测试_5分钟后", int(time.time()) + 5 * 60, "email", "L_R_no_repeat"),
        # ("正案例_任务时间测试_1小时后", int(time.time()) + 60 * 60, "email", "L_R_no_repeat"),
        # ("正案例_任务时间测试_24小时后", int(time.time()) + 24 * 60 * 60, "email", "L_R_no_repeat"),
        # ("正案例_任务时间测试_3天后", int(time.time()) + 3 * 24 * 60 * 60, "email", "L_R_no_repeat"),
        # ("正案例_任务时间测试_3天后", int(time.time()) + 3 * 24 * 60 * 60, "email", "L_R_no_repeat"),
        # ("正案例_任务时间测试_3天后", int(time.time()) + 3 * 24 * 60 * 60, "email", "L_R_no_repeat", 1000075),
        # ("正案例_任务时间测试_3天后", int(time.time()) + 3 * 24 * 60 * 60, "email", "L_R_no_repeat", 1000045),
        # ("正案例_任务时间测试_3天后", int(time.time()) + 3 * 24 * 60 * 60, "email", "L_R_no_repeat", 1000154),
        # ("正案例_任务时间测试_3天后", int(time.time()) + 3 * 24 * 60 * 60, "email", "L_R_no_repeat", 1000109),
        # ("正案例_任务时间测试_4天后", int(time.time()) + 4 * 24 * 60 * 60, "email", "L_R_no_repeat"),
        # ("正案例_任务时间测试_5天后", int(time.time()) + 5 * 24 * 60 * 60, "email", "L_R_no_repeat"),
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

    @pytest.mark.parametrize("case_name,send_time,channel,template_name,category,user_key", [
        ("正案例_邮件类型测试_fellow_contact_recipient", int(time.time()) + 24 * 60 * 60, "email", "L_R_no_repeat", "fellow_contact", "recipient"),
        ("正案例_邮件类型测试_marketing_email_user_id", int(time.time()) + 24 * 60 * 60, "email", "L_R_no_repeat", "marketing_email", "user_id"),
        ("正案例_邮件类型测试_fellow_contact_recipient", int(time.time()) + 24 * 60 * 60, "email", "L_R_no_repeat", "fellow_contact", "account_id"),
    ])
    def test_create_task_eu(self, env, cmdopt, mysql, case_name, send_time, channel, template_name, category, user_key, prepare_template, prepare_eu_email_account):
        if cmdopt not in ["test_marcopolo", "stg_marcopolo"]:
            return 0
        region = "eu"
        push_type = "email"
        service_type = region
        user_keys = "recipients"
        user_values = f"{prepare_eu_email_account[0].get(user_key)},{prepare_eu_email_account[1].get(user_key)}"
        task_detail = generate_task_detail(env, mysql, push_type, service_type, template_name, user_keys, user_values)
        json_content = {
            "execution_data": json.dumps(task_detail),
            "appointment_time": send_time,
        }
        if not json_content.get("appointment_time"):
            json_content.pop("appointment_time")
        with allure.step(f'创建发送任务接口'):
            inputs = {
                "host": env['host']['app_in'],
                "path": create_task_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "eu", "lang": "zh-cn", "hash_type": "sha256", "app_id": server_app_id, "sign": ""},
                "json": json_content
            }
            response = hreq.request(env, inputs)
            assert response.get("result_code") == "success"
            task_id = response.get("data")
        with allure.step(f'校验mysql中状态改为0'):
            mysql_result = mysql['nmp_app'].fetch("message_task", {"id": task_id})
            assert len(mysql_result) == 1
        with allure.step(f'清除测试数据'):
            if "test" in cmdopt:
                mysql['nmp_app'].delete("message_task", {"id": task_id})

    @pytest.mark.parametrize("case_name,send_time,push_type,service_type,template_name,user_data_type", [
        # ("正案例_任务时间测试__5分钟前", int(time.time()) - 5 * 60, "email", "cn", "L_R_no_repeat", "recipients"),
        # ("正案例_任务时间测试_当前时间", int(time.time()), "email", "cn", "L_R_no_repeat", "user_ids"),
        # ("正案例_任务时间测试_当前时间", int(time.time()), "email", "cn", "L_R_no_repeat", "recipients"),
        ("正案例_任务时间测试_当前时间email", int(time.time()), "email", "employee", "L_R_no_repeat", "recipients"),
        # ("正案例_任务时间测试_当前时间sms", int(time.time()), "sms", "cn", "SMS_L_R_no_repeat", "user_ids"),
        # ("正案例_任务时间测试_当前时间app", int(time.time()), "app", "cn", "APP_L_R_no_repeat", "account_ids"),
        # ("正案例_任务时间测试_4天后", int(time.time()) + 4 * 24 * 60 * 60, "email", "cn", "L_R_no_repeat", "account_ids"),
    ])
    def test_create_task_all(self, env, mysql, case_name, send_time, push_type, service_type, template_name, user_data_type):
        # todo email sms notify account
        user_data = env["notify_account"][push_type][service_type][user_data_type]
        app_id = 10000
        task_detail = generate_task_detail(env, mysql, push_type, service_type, template_name, user_data_type, user_data)
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
        task_id = response.get("data")
        with allure.step(f'清除测试数据'):
            mysql['nmp_app'].delete("message_task", {"id": task_id})
        if response.get("result_code") == "success":
            return response.get("data")
        else:
            return response

    create_task_keys = "case_name,send_time,channel,template_name,snapshot,operate"
    create_task_cases = [
        ("正案例_任务时间测试_1分钟后_创建任务后更新模板", int(time.time()) + 1 * 60, "email", "L_R_no_repeat_p_update", True, "update"),
        ("正案例_任务时间测试_不定时_创建任务后删除模板", None, "email", "L_R_no_repeat_p_delete", True, "delete"),
        ("正案例_任务时间测试_不定时_不修改模板", None, "email", "L_R_no_repeat_p_snapshot", True, None),
    ]
    create_task_ids = [f"{case[0]}" for case in create_task_cases]

    @pytest.mark.parametrize(create_task_keys, create_task_cases, ids=create_task_ids)
    def test_create_task_snapshot(self, env, cmdopt, mysql, case_name, send_time, channel, template_name, snapshot, operate):
        region_list = ["cn", "employee"]
        if "marcopolo" in cmdopt:
            region_list = ["eu", "employee"]
        for region in region_list:
            recipients = recipients_map.get(region)
            user_keys = "recipients"
            with allure.step(f'创建发送任务接口'):
                push_type = "email"
                service_type = region
                task_detail = generate_task_detail(env, mysql, push_type, service_type, template_name, user_keys, recipients, snapshot)
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
                template_id = task_detail.get("push_data").get("template_id")

            with allure.step(f'校验mysql'):
                mysql_task = mysql['nmp_app'].fetch("message_task", {"id": task_id})
                assert len(mysql_task) == 1
                execution_data = eval(mysql_task[0].get("execution_data"))
                version_mysql = execution_data.get('push_data').get('version')
                if not snapshot:
                    template_snapshot = mysql["nmp_app"].fetch("message_template_snapshot", {"template_id": template_id}, suffix="order by create_time")
                    template_version = template_snapshot[0].get("version")
                    assert template_version == version_mysql
                else:
                    task_version = task_detail.get('push_data').get('version')
                    assert task_version == version_mysql
        with allure.step("创建任务后更新模板状态以及内容"):
            if operate == "update":
                update_template(env, mysql, template_id, template_name=template_name)
            elif operate == "delete":
                delete_template(env, mysql, template_id)

    @pytest.mark.parametrize("case_name,app_id,id_type,channel", [
        ("正案例_已发布的模板不允许修改", "10000", "published", "email"),
        ("反案例_未发布的模板", "10000", "new", "email"),
        ("反案例_不存在的模板", "10000", "not_exist", "email"),
        ("反案例_为None", "10000", "None", "email"),
    ])
    def test_create_task_by_template_status(self, env, mysql, cmdopt, case_name, app_id, id_type, channel):
        if id_type == "new":
            template_id = create_new_template(env, mysql).get("id")
        elif id_type == "published":
            template_id = get_published_template_id(env, mysql)
        else:
            template_id_map = {"None": None, "not_exist": -1}
            template_id = template_id_map.get(id_type)
        with allure.step('创建任务接口'):
            region_list = ["cn", "employee"]
            if "marcopolo" in cmdopt:
                region_list = ["eu", "employee"]
            for region in region_list:
                with allure.step(f'创建发送任务接口'):
                    json_con = {
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
                    inputs = {
                        "host": env['host']['app_in'],
                        "path": create_task_path,
                        "method": "POST",
                        "headers": {"Content-Type": "application/json"},
                        "params": {"region": region, "lang": "zh-cn", "hash_type": "sha256", "app_id": 10000, "sign": ""},
                        "json": {
                            "execution_data": json.dumps(json_con),
                        }
                    }
                    response = hreq.request(env, inputs)
                    if "正案例" in case_name:
                        assert response.get("result_code") == "success"
                    else:
                        assert response.get("result_code") == "invalid_param"

    create_task_by_tag_keys = "case_name,send_time,channel,template_name,service_type,tag_name"
    create_task_by_tag_cases = [
        ("正案例_email标签cn", int(time.time()), "email", "no_variable", "cn", "init_email"),
        ("正案例_email标签eu", int(time.time()), "email", "no_variable", "eu", "init_email"),
        ("正案例_user_id标签eu", int(time.time()), "email", "no_variable", "eu", "init_user_id"),
        ("正案例_account_id标签eu", int(time.time()), "email", "no_variable", "eu", "init_account_id"),
    ]
    create_task_by_tag_ids = [f"{case[0]}" for case in create_task_by_tag_cases]

    @pytest.mark.parametrize(create_task_by_tag_keys, create_task_by_tag_cases, ids=create_task_by_tag_ids)
    def test_create_task_by_tag(self, env, cmdopt, mysql, case_name, send_time, channel, template_name, service_type, tag_name, prepare_tag):
        if "marcopolo" in cmdopt and service_type == "cn":
            logger.debug("marco polo 环境不运行cn案例")
            return 0
        if "marcopolo" not in cmdopt and service_type == "eu":
            logger.debug("非marco polo 环境不运行eu案例")
            return 0
        with allure.step(f'创建发送任务接口'):
            task_detail = generate_task_detail(env, mysql, channel, service_type, template_name, "tag_id", prepare_tag.get(tag_name))
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
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": 10000, "sign": ""},
                "json": json_content
            }
            response = hreq.request(env, inputs)
            assert response.get("result_code") == "success"
            task_id = response.get("data")
        with allure.step(f'校验mysql中状态改为0'):
            mysql_result = mysql['nmp_app'].fetch("message_task", {"id": task_id})
            assert len(mysql_result) == 1
