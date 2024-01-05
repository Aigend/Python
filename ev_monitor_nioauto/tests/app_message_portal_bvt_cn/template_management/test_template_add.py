# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_template_add.py
# @Author : qiangwei.zhang
# @time: 2021/07/29
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import time
import json
import pytest

from utils.assertions import assert_equal
from utils.random_tool import random_string
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from data.email_content import template_str_text, html5_new1, markdown_file_img ,wechat_applet_template_dict
from tests.app_message_portal.template_management.template_server import init_feishu_template
from tests.app_message_portal.template_management.template_server import init_variable, init_email_template, \
    init_sms_template

add_template_path = "/api/2/in/message_portal/template/add"
app_id = 10000


# app_id = '100480'


def init_template(env, mysql):
    res = init_variable(env, mysql)
    logger.debug(res)
    res2 = init_email_template(env, mysql)
    logger.debug(res2)
    res3 = init_sms_template(env, mysql)
    logger.debug(res3)
    res4 = init_feishu_template(env, mysql)
    logger.debug(res4)


@pytest.mark.parametrize("case_name,channel,template_type,template_name,template_str", (
        ["正案例_email_text", "email", "text", f"【新增模板名称】_{random_string(13)}", template_str_text],
        ["正案例_im_text", "im", "text", f"【新增模板名称】_{random_string(13)}", template_str_text],
        ["正案例_email_H5", "email", "H5", f"【新增模板名称】_{random_string(13)}", html5_new1],
        ["正案例_sms_text", "sms", "text", f"【新增模板名称】_{random_string(13)}", template_str_text],
        ["正案例_sms_text", "sms", "text", "短信模板", template_str_text],
        ["正案例_web_text", "web", "text", f"【新增模板名称】_{random_string(13)}", template_str_text],
        ["正案例_app_text", "app", "text", f"【新增模板名称】_{random_string(13)}", template_str_text],
        ["正案例_feishu_text", "feishu", "text", f"【新增模板名称】_{random_string(13)}", markdown_file_img],
        ["正案例_voice_text_alarm", "voice", "text", f"【新增模板名称】_voice_alarm_{random_string(13)}", markdown_file_img],
        ["正案例_voice_text", "voice", "text", f"【新增模板名称】_{random_string(13)}", markdown_file_img],
        ["正案例_wechat_applet", "wechat_applet", "text", f"【新增模板名称】_{random_string(13)}", wechat_applet_template_dict],
))
def test_add_template(env, cmdopt, mysql, case_name, channel, template_type, template_name, template_str):
    cmdopt = env["cmdopt"]
    voice_category = "notification"
    if template_name:
        voice_category = "alarm" if "voice_alarm" in template_name else "notification"
    target_app_ids = "10001,10002"
    if "marcopolo" in cmdopt:
        target_app_ids = "1000003,1000004"
    template_channel_map = {
        "email": {
            "subject": f"邮件模板初始化发送{template_name}",
            "content": f"亲爱的【[*qa_user_name*]】你好，这是portal服务模板，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消!{template_str}",
            "category": "fellow_contact",
            "sender_name": "notification@nio.com",
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境模板"
            }, ensure_ascii=False)
        },
        "sms": {
            "content": f"亲爱的【[*qa_user_name*]】你好，这是portal服务模板，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消!{template_str}",
            "category": "ads",
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境短信模板"
            }, ensure_ascii=False)
        },
        "voice": {
            "content": f"亲爱的【[*qa_user_name*]】你好，这是portal服务模板，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消!{template_str}",
            "category": voice_category,
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】语音环境短信模板"
            })
        },
        "app": {
            "payload": json.dumps({
                "content": f"{template_str} app模板",
                "target_link": "http://www.niohome.com",
                "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "title": f"【{cmdopt}】环境,模板推送.{channel}渠道推送"
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
                "title": f"【{cmdopt}】环境{channel}渠道推送[#test_variable#]",
                "content": f"亲爱的【[*qa_user_name*]】你好，这是portal服务模板，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消!{template_str}",
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
            "title": f"【{cmdopt}】环境,portal服务模板推送飞书",
            "content": f"亲爱的【[*qa_user_name*]】你好，这是飞书模板，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消!{template_str}",
            "url": "https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN",
            "sender_name": "test sender_name",
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境,feishu初始化模板",
                "content": template_str
            }, ensure_ascii=False)
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
                            'buttons': [
                                {'text': 'Check details', 'app_link': '[#app_link#]', 'web_link': '[#web_link#]'}],
                            'ext_data': {},
                            'resource': [
                                {'id': 1, 'highlight': True, 'resource_type': 1, 'account_id': '[#account_id1#]'},
                                {'id': 2, 'highlight': True, 'resource_type': 2, 'text': 'Puyang', 'app_link': 'xxx',
                                 'web_link': 'xxx'},
                                {'id': 3, 'highlight': True, 'resource_type': 3, 'account_id': '[#account_id2#]',
                                 'app_link': 'xxx', 'web_link': 'xxx'}
                            ]
                        }
                    })
                }
            }], ensure_ascii=False),
            "sync_other_machine": 1,
            "cloud_custom_data": str(json.dumps({
                'version': '0.1',
                'platform': 'taitan',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                'business_code': '1.1',
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
        },
        "wechat_applet": {
            # TcxtCB1C9J-6ucVV5dgi4ehDva__1u8BvaB3bz-Xw1w是业务方提供的微信模版id，包含四个key: date1 thing2 number3 thing4
            "template_id": "TcxtCB1C9J-6ucVV5dgi4ehDva__1u8BvaB3bz-Xw1w",
            "data": template_str,
            "page": "test url",
            "properties": "any properties you want, you can store a json here"
        }
    }
    template_content = template_channel_map.get(channel)
    logger.debug(f"template_content{template_content}")
    if not template_content:
        template_content = {"error": "模板类型错误"}
    with allure.step('添加消息模版接口'):
        inputs = {
            "host": env['host']['app_in'],
            "path": add_template_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": "",
            },
            "json": {
                "channel": channel,
                "name": template_name,
                "type": template_type,
                "template_str": json.dumps(template_content, ensure_ascii=False),
            }
        }
        if not template_str:
            inputs["json"].pop("template_str")
        if not template_type:
            inputs["json"].pop("type")
        if not template_name:
            inputs["json"].pop("name")

        logger.debug(inputs)

        response = hreq.request(env, inputs)
        if "正案例" in case_name:
            with allure.step("校验是否包含contain illegal word"):
                if response.get("debug_msg"):
                    if "contain illegal word" in response.get("debug_msg"):
                        logger.info("contain illegal word,skip case result verify")
                        return 0
            assert response['result_code'] == 'success'
            template = mysql["nmp_app"].fetch("message_template", {"name": template_name},
                                              suffix="order by create_time desc")
            template_id = response.get("data")
            # assert channel.upper() in template_id
            template_id_mysql = template[0].get("template_id")
            assert str(template_id) == str(template_id_mysql)
            template_snapshot = mysql["nmp_app"].fetch("message_template_snapshot", {"template_id": template_id})
            assert template_snapshot
            assert len(template_snapshot) == 1
            logger.debug(f'template_id:{template_id}')
            with allure.step("校验更新后message_template表模板内容正确"):
                template = mysql["nmp_app"].fetch("message_template", where_model={"template_id": template_id}, )
                mysql_value_template = {
                    'channel': channel,
                    "template_str": bytes.decode(template[0].get("template")),
                    "name": template[0].get("name"),
                    "type": template[0].get("type"),
                }
                assert_equal(mysql_value_template, inputs.get("json"))
            with allure.step("校验更新后message_template_snapshot表模板内容正确"):
                template_snapshot = mysql["nmp_app"].fetch("message_template_snapshot", {"template_id": template_id},
                                                           suffix="order by create_time desc")
                mysql_value_template_snapshot = {
                    'channel': channel,
                    "template_str": bytes.decode(template_snapshot[0].get("template")),
                    "name": template_name,
                    "type": template_type,
                }
                assert_equal(mysql_value_template_snapshot, inputs.get("json"))
        else:
            assert response['result_code'] == 'invalid_param'

