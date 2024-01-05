# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_update_template.py
# @Author : qiangwei.zhang
# @time: 2021/07/29
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述
import time
import json
import pytest
import allure
from utils.random_tool import random_string, format_time
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_portal.template_management.template_server import create_new_template, get_published_template_id
from utils.assertions import assert_equal


@pytest.mark.parametrize("case_name,app_id,id_type,channel", [
    ("正案例_未发布的模板", "10000", "new", "email"),
    # ("正案例_未发布的模板", "10000", "new", "app"),
    # ("正案例_未发布的模板", "10000", "new", "sms"),
    # ("正案例_未发布的模板", "10000", "new", "voice"),
    # ("正案例_未发布的模板", "10000", "new", "im"),
    # ("正案例_未发布的模板", "10000", "new", "feishu"),
    # ("正案例_未发布的模板", "10000", "new", "web"),
    # ("反案例_已发布的模板不允许修改", "10000", "published", "email"),
])
def test_update_template(env, mysql, case_name, app_id, id_type, channel):
    voice_category = "notification"
    if id_type == "new":
        template_id = create_new_template(env, mysql, channel=channel).get("template_id")
        time.sleep(1)  # 创建完成后1秒再更新 UNIQUE KEY `template_version_key` (`template_id`,`version`)
    elif id_type == "published":
        template_id = get_published_template_id(env, mysql)
    if case_name.startswith("正案例"):
        template_snapshot = mysql["nmp_app"].fetch("message_template_snapshot", {"template_id": template_id}, {"count(1) template_count"})
        template_snapshot_count_before_update = template_snapshot[0].get("template_count")
    with allure.step('更新模板接口'):
        """
        http://showdoc.nevint.com/index.php?s=/647&page_id=31041
        """
        cmdopt = env["cmdopt"]
        template_name = f"自动化脚本更新{random_string(13)}"
        template_str = "模板更新"
        target_app_ids = "10001,10002"
        if "marcopolo" in cmdopt:
            target_app_ids = "1000003,1000004"
        template_channel_map = {
            "email": {
                "subject": f"SB邮件模板初始化发送{template_name}",
                "content": f"亲爱的【[*qa_user_name*]】你好，这是portal服务模板测试，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消!{template_str}",
                "category": "fellow_contact",
                "sender_name": "notification@nio.com",
                "properties": json.dumps({
                    "source": "QA_TEST",
                    "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "case_name": f"【{cmdopt}】环境模板测试"
                }, ensure_ascii=False)
            },
            "sms": {
                "content": f"亲爱的【[*qa_user_name*]】你好，这是portal服务模板测试，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消!{template_str}",
                "category": "ads",
                "properties": json.dumps({
                    "source": "QA_TEST",
                    "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "case_name": f"【{cmdopt}】环境短信模板测试"
                }, ensure_ascii=False)
            },
            "voice": {
                "content": f"亲爱的【[*qa_user_name*]】你好，这是portal服务模板测试，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消!{template_str}",
                "category": voice_category,
                "properties": json.dumps({
                    "source": "QA_TEST",
                    "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "case_name": f"【{cmdopt}】语音环境短信模板测试"
                }, ensure_ascii=False)
            },
            "app": {
                "payload": json.dumps({
                    "content": f"{template_str} app模板",
                    "target_link": "http://www.niohome.com",
                    "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "title": f"【{cmdopt}】环境,模板推送测试.{channel}渠道推送测试"
                }, ensure_ascii=False),
                "scenario": "ls_link",
                "ttl": "100000",
                "target_app_ids": target_app_ids,
                "category": "default",
                "store_history": "false",
                "pass_through": "0",
                "do_push": "true",
                "channel": "all",
                "properties": json.dumps({
                    "source": "QA_TEST",
                    "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "case_name": f"【{cmdopt}】环境,app初始化模板",
                    "content": template_str
                }, ensure_ascii=False)
            },
            "web": {
                "payload": json.dumps({
                    "target_link": "http://www.niohome.com",
                    "description": f"[#description#]时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "title": f"【{cmdopt}】环境{channel}渠道推送测试[#test_variable#]",
                    "content": f"亲爱的【[*qa_user_name*]】你好，这是portal服务模板测试，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消!{template_str}",
                }, ensure_ascii=False),
                "scenario": "ls_link",
                "ttl": "100000",
                "target_app_ids": target_app_ids,
                "category": "default",
                "store_history": "true",
                "pass_through": "0",
                "do_push": "true",
                "channel": "all",
                "properties": json.dumps({
                    "source": "QA_TEST",
                    "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "case_name": f"【{cmdopt}】环境,app初始化模板",
                    "content": template_str
                }, ensure_ascii=False)
            },
            "feishu": {
                "title": f"【{cmdopt}】环境,portal服务模板推送飞书测试",
                "content": f"亲爱的【[*qa_user_name*]】你好，这是飞书模板测试，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消!{template_str}",
                "url": "https://open.feishu.cn",
            },
            "im": {
                'from': "test",
                'msg_body': json.dumps([{
                    'MsgType': 'TIMCustomElem',
                    'MsgContent': {
                        'Data': str({
                            'major_type': 3,
                            'sub_type': 1,
                            'major': {
                                'title': f'User Service{template_str}',
                                'status': 1,
                                'text': '${1} order vehicle has been unbound by ${2}',
                                'text_placeholder': [{'start_index': 0, 'length': 4}, {'start_index': 39, 'length': 4}],
                                'buttons': [{'text': 'Check details', 'app_link': '[#app_link#]', 'web_link': '[#web_link#]'}],
                                'ext_data': {},
                                'resource': [
                                    {'id': 1, 'highlight': True, 'resource_type': 1, 'account_id': '[#account_id1#]'},
                                    {'id': 2, 'highlight': True, 'resource_type': 2, 'text': 'Puyang', 'app_link': 'xxx', 'web_link': 'xxx'},
                                    {'id': 3, 'highlight': True, 'resource_type': 3, 'account_id': '[#account_id2#]', 'app_link': 'xxx', 'web_link': 'xxx'}
                                ]
                            }
                        })
                    }
                }], ensure_ascii=False),
                "sync_other_machine": 1,
                "cloud_custom_data": str(json.dumps({
                    'version': '0.1',
                    'platform': 'taitan',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36', 'business_code': '1.1',
                    'function': {
                        'filter': ['nio_cn'],
                        'delete': ['nio_cn']
                    }
                })),
                "status": 1,
                "properties": json.dumps({
                    "source": "QA_TEST",
                    "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "case_name": f"【{cmdopt}】环境,feishu初始化模板",
                    "content": template_str
                }, ensure_ascii=False)
            }
        }
        template_content = template_channel_map.get(channel)
        if not template_content:
            template_content = {"error": "模板类型错误"}
        path = "/api/2/in/message_portal/template/update"
        rs5 = random_string(5)
        ft = format_time()
        name = f"【更新模板名称】{rs5}_{ft}"
        http = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                "id": template_id,
                "template_str": json.dumps(template_content, ensure_ascii=False),
                "name": name,
            }
        }
        response = hreq.request(env, http)
        with allure.step("校验是否包含contain illegal word"):
            if response.get("debug_msg"):
                if "contain illegal word" in response.get("debug_msg"):
                    logger.info("contain illegal word,skip case result verify")
                    return 0
        if case_name.startswith("正案例"):
            time.sleep(5)
            with allure.step("校验更新后message_template表模板内容正确"):
                assert response['result_code'] == 'success'
                template = mysql["nmp_app"].fetch("message_template", {"template_id": template_id}, )
                mysql_value_template = {
                    "id": template[0].get("template_id"),
                    "template_str": bytes.decode(template[0].get("template")),
                    "name": template[0].get("name"),
                }
                assert_equal(mysql_value_template, http.get("json"))
            with allure.step("校验更新后message_template_snapshot表模板内容正确"):
                template_snapshot = mysql["nmp_app"].fetch("message_template_snapshot", {"template_id": template_id}, suffix="order by create_time desc")
                mysql_value_template_snapshot = {
                    "id": template_snapshot[0].get("template_id"),
                    "template_str": bytes.decode(template_snapshot[0].get("template")),
                    "name": name,
                }
                assert_equal(mysql_value_template_snapshot, http.get("json"))
            with allure.step("校验更新后快照数量比更新前+1"):
                template_snapshot = mysql["nmp_app"].fetch("message_template_snapshot", {"template_id": template_id}, {"count(1) template_count"})
                template_snapshot_count_after_update = template_snapshot[0].get("template_count")
                assert template_snapshot_count_after_update == template_snapshot_count_before_update + 1
        else:
            if template_id:
                response.pop("request_id")
                response.pop("server_time")
                expected_res = {
                    "result_code": "invalid_param",
                    "debug_msg": "template should in draft status before update",
                }
                if template_id == -1 or id_type == "deleted":
                    expected_res = {
                        "result_code": "invalid_param",
                        "debug_msg": "invalid template id"
                    }
                assert_equal(expected_res, response)
            else:
                response.pop("server_time")
                response.pop("request_id")
                expected_res = {
                    "result_code": "invalid_param",
                    "debug_msg": "necessary parameters are null."
                }
                assert_equal(expected_res, response)