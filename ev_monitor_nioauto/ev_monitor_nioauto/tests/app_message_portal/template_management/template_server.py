# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : template_server.py
# @Author : qiangwei.zhang
# @time: 2021/08/02
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述
import functools

import allure
import json
import time
from utils.random_tool import random_string, format_time
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_portal.variable_management.variable_server import init_variable
from data.email_content import H5_R_L, nuwa_policy_h5

add_template_path = "/api/2/in/message_portal/template/add"
publish_template_path = "/api/2/in/message_portal/template/publish"
offline_template_path = "/api/2/in/message_portal/template/offline"
delete_template_path = "/api/2/in/message_portal/template/delete"
detail_template_path = "/api/2/in/message_portal/template/detail"


def create_new_template(env, mysql, channel="email", content_type='text', app_id=10000):
    res = create_template(env, mysql, channel, content_type, app_id)
    if not res:
        num = 5
        while True:
            num = num - 1
            res = create_template(env, mysql, channel, content_type, app_id)
            if res or num <= 0:
                break
    return res


def create_template(env, mysql, channel="email", content_type='text', app_id=10000):
    cmdopt = env["cmdopt"]
    template_name = f"{channel}_{content_type}_自动化脚本创建{random_string(13)}"
    template_str = "模板创建"
    target_app_ids = "10001,10002"
    if "marcopolo" in cmdopt:
        target_app_ids = "1000003,1000004"
    template_channel_map = {
        "email": {
            "subject": f"邮件模板初始化发送{template_name}",
            "content": template_str,
            "category": "fellow_contact",
            "sender_name": "notification@nio.io" if "marcopolo" in cmdopt else "notification@nio.com",
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境模板测试"
            })
        },
        "sms": {
            "content": template_str,
            "category": "ads",
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境短信模板测试"
            })
        },
        "voice": {
            "content": template_str,
            "category": "notification",
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】语音环境短信模板测试"
            })
        },
        "app": {
            "payload": json.dumps({
                "content": template_str,
                "target_link": "http://www.niohome.com",
                "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "title": f"【{cmdopt}】环境,模板推送测试.{channel}渠道推送测试"
            }),
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
            })
        },
        "web": {
            "payload": json.dumps({
                "target_link": "http://www.niohome.com",
                "description": f"[#description#]时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "title": f"【{cmdopt}】环境{channel}渠道推送测试[#test_variable#]",
                "content": template_str,
            }),
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
            })
        },
        "feishu": {
            "title": f"【{cmdopt}】环境,portal服务模板推送飞书测试",
            "content": f"亲爱的【[*qa_user_name*]】你好，这是飞书模板测试，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消![图片gif](img_v2_fe42028a-9ebf-477f-bf97-4c95b0eb22eg)![图片png](img_v2_143c32b9-f08b-4788-b2ae-e55801c3af2g)",
            "url": "http://www.niohome.com",
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境,im初始化模板",
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
            # 'status': 1,
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境,im初始化模板",
                "content": template_str
            }, ensure_ascii=False)
        }
    }
    template_content = template_channel_map.get(channel)
    if not template_content:
        template_content = {"error": "模板类型错误"}
    with allure.step('添加消息模版接口'):
        inputs = {
            "host": env['host']['app_in'],
            "path": add_template_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ''},
            "json": {
                "channel": channel,
                "name": template_name,
                "type": content_type,
                "template_str": json.dumps(template_content),
            }
        }
        response = hreq.request(env, inputs)
        if response['result_code'] != 'success':
            return False
        template_id = response.get("data")
        template = mysql["nmp_app"].fetch("message_template", {"template_id": template_id, "valid": 1})
        logger.debug(f'template_id:{template_id}')
        return template[0]


def get_published_template_id(env, mysql, app_id=10000):
    template = mysql["nmp_app"].fetch("message_template", {"status": 9, "app_id": app_id}, "order by create_time desc")
    if template:
        return template[0].get("template_id")
    else:
        new_template_id = create_new_template(env, mysql).get("template_id")
        with allure.step(f'消息模版接口:{publish_template_path}'):
            http = {
                "host": env['host']['app_in'],
                "path": publish_template_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": {"id": new_template_id}
            }
            response = hreq.request(env, http)
            assert response['result_code'] == 'success'
            with allure.step('校验mysql模板状态为9已发布'):
                template = mysql["nmp_app"].fetch("message_template", {"status": 9, "template_id": new_template_id, "valid": 1})
                assert len(template) == 1
                return new_template_id


def get_deleted_template_id(env, mysql, app_id=10000):
    template = mysql["nmp_app"].fetch("message_template", {"valid": 0, "app_id": app_id, "valid": 1}, "order by create_time desc")
    if template:
        return template[0].get("template_id")
    else:
        new_template_id = create_new_template(env, mysql).get("template_id")
        with allure.step(f'消息模版接口:{delete_template_path}'):
            http = {
                "host": env['host']['app_in'],
                "path": delete_template_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": {"id": new_template_id}
            }
            response = hreq.request(env, http)
            assert response['result_code'] == 'success'
            with allure.step('校验mysqlvalid为0已删除'):
                template = mysql["nmp_app"].fetch("message_template", {"valid": 0, "template_id": new_template_id})
                assert len(template) == 1
                return new_template_id


def published_template(env, mysql, template_id, app_id=10000):
    template = mysql["nmp_app"].fetch("message_template", {"status": 9, "template_id": template_id, "valid": 1}, retry_num=2)
    if template:
        return f"模板{template_id}已是发布状态"
    else:
        with allure.step(f'消息模版接口:{publish_template_path}'):
            http = {
                "host": env['host']['app_in'],
                "path": publish_template_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": {"id": template_id}
            }
            response = hreq.request(env, http)
            assert response['result_code'] == 'success'
            with allure.step('校验mysql模板状态为9已发布'):
                template = mysql["nmp_app"].fetch("message_template", {"status": 9, "template_id": template_id, "valid": 1}, retry_num=30)
                assert len(template) == 1
            return f"模板{template_id}已发布"


def update_template(env, mysql, template_id, app_id=10000, template_name=None):
    template = mysql["nmp_app"].fetch("message_template", {"template_id": template_id, "valid": 1}, retry_num=2)
    voice_category = "alarm" if "voice_alarm" in template_name else "notification"
    if template[0].get("status") == "9":
        offline_template(env, mysql, template_id, app_id)
    cmdopt = env['cmdopt']
    channel = template[0].get("channel")
    with allure.step(f'消息模版接口:{publish_template_path}'):
        if not template_name:
            template_name = f"自动化脚本更新{random_string(13)}"
        template_str = "模板更新"
        target_app_ids = "10001,10002"
        if "marcopolo" in cmdopt:
            target_app_ids = "1000003,1000004"
        template_channel_map = {
            "email": {
                "subject": f"邮件模板初始化发送{template_name}",
                "content": template_str,
                "category": "fellow_contact",
                "sender_name": "notification@nio.io" if "marcopolo" in cmdopt else "notification@nio.com",
                "properties": json.dumps({
                    "source": "QA_TEST",
                    "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "case_name": f"【{cmdopt}】环境模板测试"
                })
            },
            "sms": {
                "content": template_str,
                "category": "ads",
                "properties": json.dumps({
                    "source": "QA_TEST",
                    "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "case_name": f"【{cmdopt}】环境短信模板测试"
                })
            },
            "voice": {
                "content": template_str,
                "category": voice_category,
                "properties": json.dumps({
                    "source": "QA_TEST",
                    "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "case_name": f"【{cmdopt}】语音环境短信模板测试"
                })
            },
            "app": {
                "payload": json.dumps({
                    "content": template_str,
                    "target_link": "http://www.niohome.com",
                    "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "title": f"【{cmdopt}】环境,模板推送测试推送测试"
                }),
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
                })
            },
            "web": {
                "payload": json.dumps({
                    "target_link": "http://www.niohome.com",
                    "description": f"[#description#]时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "title": f"【{cmdopt}】环境渠道推送测试[#test_variable#]",
                    "content": template_str,
                }),
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
                })
            },
            "feishu": {
                "title": f"【{cmdopt}】环境,portal服务模板推送飞书测试",
                "content": f"亲爱的【[*qa_user_name*]】你好，这是飞书模板测试，名字是随机生成的，如有打扰请见谅，可联系qiangwei.zhang@nio.com取消![图片gif](img_v2_fe42028a-9ebf-477f-bf97-4c95b0eb22eg)![图片png](img_v2_143c32b9-f08b-4788-b2ae-e55801c3af2g)",
                "url": "https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN"
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
                                # 'status': 1,
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
                # 'status': 1,
                "properties": json.dumps({
                    "source": "QA_TEST",
                    "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "case_name": f"【{cmdopt}】环境,im初始化模板",
                    "content": template_str
                }, ensure_ascii=False)
            }
        }
        template_content = template_channel_map.get(channel)
        if not template_content:
            template_content = {"error": "模板类型错误"}
        path = "/api/2/in/message_portal/template/update"
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
                "template_str": json.dumps(template_content),
                "name": template_name,
            }
        }
        response = hreq.request(env, http)
        return response


def offline_template(env, mysql, template_id, app_id=10000):
    template = mysql["nmp_app"].fetch("message_template", {"status": 1, "template_id": template_id, "valid": 1}, retry_num=2)
    if template:
        return f"模板{template_id}已是草稿状态"
    else:
        with allure.step(f'消息模版接口:{offline_template_path}'):
            http = {
                "host": env['host']['app_in'],
                "path": offline_template_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": {"id": template_id}
            }
            response = hreq.request(env, http)
            assert response['result_code'] == 'success'
            with allure.step('校验mysql模板状态为9已发布'):
                template = mysql["nmp_app"].fetch("message_template", {"status": 1, "template_id": template_id, "valid": 1}, retry_num=30)
                assert len(template) == 1
            return f"模板{template_id}已下线"


def delete_template(env, mysql, template_id, app_id=10000):
    template = mysql["nmp_app"].fetch("message_template", {"template_id": template_id, "valid": 1})
    if template:
        if template[0].get("status") == 9:
            offline_template(env, mysql, template_id, app_id)
        with allure.step('删除消息模版接口'):
            http = {
                "host": env['host']['app_in'],
                "path": delete_template_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": {"id": template_id}
            }
            response = hreq.request(env, http)
            assert response['result_code'] == "success"
            with allure.step('校验mysql模板被删除'):
                template = mysql["nmp_app"].fetch("message_template", {"valid": 1, "template_id": template_id}, retry_num=1)
                assert len(template) == 0
                return "success"
    else:
        return "模板不存在或已发布不可被删除"


def get_template_detail(env, template_id, app_id=10000):
    with allure.step('根据id获取消息模板详情接口'):
        http = {
            "host": env['host']['app_in'],
            "path": detail_template_path,
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn",
                       "lang": "zh-cn",
                       "hash_type": "sha256",
                       "app_id": app_id,
                       'id': template_id,
                       "sign": ""
                       }
        }
        response = hreq.request(env, http)
        logger.debug(response)
        assert response['result_code'] == 'success'
        return response


def create_template_and_published(env, mysql, channel="email", content_type="text", template_name="qa_autotest_create", template_str="autotest new template", app_id=10000):
    cmdopt = env["cmdopt"]
    voice_category = "alarm" if "voice_alarm" in template_name else "notification"
    target_app_ids = "10001,10002"
    if "marcopolo" in cmdopt:
        if "_TOB_" in template_name:
            target_app_ids = "1000014,100417"
        else:
            target_app_ids = "1000003,1000004"
    else:
        if "_TOB_" in template_name:
            target_app_ids = "10003"
    template_channel_map = {
        "email": {
            "subject": f"邮件模板初始化发送{template_name}",
            "content": f"{template_name}_{template_str}",
            "category": "fellow_contact",
            "sender_name": "notification@nio.io" if "marcopolo" in cmdopt else "notification@nio.com",
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境模板测试"
            }, ensure_ascii=False)
        },
        "sms": {
            "content": f"{template_name}_{template_str}",
            "category": 'ads',
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境短信模板测试"
            }, ensure_ascii=False)
        },
        "voice": {
            "content": f"{template_str}",
            "category": voice_category,
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】语音环境短信模板测试"
            }, ensure_ascii=False)
        },
        "app": {
            "payload": json.dumps({
                "content": f"{template_name}_{template_str}",
                "target_link": "http://www.niohome.com",
                "description": f"description【[#description#]】时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "title": f"【{cmdopt}】环境,模板推送测试.{channel}渠道推送测试title【[#title#]】"
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
                "content": f"{template_name}_{template_str}"
            }, ensure_ascii=False)
        },
        "web": {
            "payload": json.dumps({
                "target_link": "http://www.niohome.com",
                "description": f"[#description#]时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "title": f"【{cmdopt}】环境{channel}渠道推送测试[#test_variable#]",
                "content": template_str,
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
                "content": f"{template_name}_{template_str}"
            }, ensure_ascii=False)
        },
        "feishu": {
            "title": f"【{cmdopt}】环境,portal服务模板推送飞书测试",
            "content": f"{template_name}_{template_str}",
            "url": "https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN"
        },
        "im": {
            # 'from': "test",
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
            # 'status': 1,
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境,im初始化模板",
                "content": template_str
            }, ensure_ascii=False)
        }
    }
    template_content = template_channel_map.get(channel)
    if not template_content:
        template_content = {"error": "模板类型错误"}
    if 'im' == channel and 'No_From' not in template_name:
        if 'test' in cmdopt:
            template_content['from'] = 'test'
        elif 'stg' in cmdopt:
            template_content['from'] = 'Task'
    template = mysql["nmp_app"].fetch("message_template", {"name": template_name, "channel": channel, "valid": 1}, retry_num=1)
    if template:
        template_id = template[0].get("template_id")
    else:
        with allure.step('添加消息模版接口'):
            inputs = {
                "host": env['host']['app_in'],
                "path": add_template_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ''},
                "json": {
                    "channel": channel,
                    "name": template_name,
                    "type": content_type,
                    "template_str": json.dumps(template_content),
                }
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
            template_id = response.get("data")
    with allure.step("发布模板"):
        published_template(env, mysql, template_id)
    return template_id


def create_published_offline_template(env, mysql, channel="email", content_type="text", template_name="qa_autotest_create", template_str="autotest new template", app_id=10000):
    cmdopt = env["cmdopt"]
    target_app_ids = "10001,10002"
    voice_category = "alarm" if "voice_alarm" in template_name else "notification"
    if "marcopolo" in cmdopt:
        target_app_ids = "1000003,1000004"
    template_channel_map = {
        "email": {
            "subject": f"邮件模板初始化发送{template_name}",
            "content": template_str,
            "category": "fellow_contact",
            "sender_name": "notification@nio.io" if "marcopolo" in cmdopt else "notification@nio.com",
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境模板测试"
            }, ensure_ascii=False)
        },
        "sms": {
            "content": f"{template_name}_{template_str}",
            "category": 'ads',
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境短信模板测试"
            }, ensure_ascii=False)
        },
        "voice": {
            "content": f"{template_name}_{template_str}",
            "category": voice_category,
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】语音环境短信模板测试"
            }, ensure_ascii=False)
        },
        "app": {
            "payload": json.dumps({
                "content": f"{template_name}_{template_str}",
                "target_link": "http://www.niohome.com",
                "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "title": f"【{cmdopt}】环境,模板推送测试.{channel}渠道推送测试"
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
                "content": f"{template_name}_{template_str}"
            }, ensure_ascii=False)
        },
        "web": {
            "payload": json.dumps({
                "target_link": "http://www.niohome.com",
                "description": f"[#description#]时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "title": f"【{cmdopt}】环境{channel}渠道推送测试[#test_variable#]",
                "content": template_str,
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
                "content": f"{template_name}_{template_str}"
            }, ensure_ascii=False)
        },
        "feishu": {
            "title": f"【{cmdopt}】环境,portal服务模板推送飞书测试",
            "content": f"{template_name}_{template_str}",
            "url": "https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN"
        }, "im": {
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
            # 'status': 1,
            "properties": json.dumps({
                "source": "QA_TEST",
                "time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "case_name": f"【{cmdopt}】环境,im初始化模板",
                "content": template_str
            }, ensure_ascii=False)
        }
    }
    template_content = template_channel_map.get(channel)
    if not template_content:
        template_content = {"error": "模板类型错误"}
    template = mysql["nmp_app"].fetch("message_template", {"name": template_name, "channel": channel, "valid": 1}, retry_num=1)
    if template:
        # 如果模板已存在将模板状态改为9，模板内容更新为最新
        template_id = template[0].get("template_id")
        if 'stg' not in cmdopt:
            mysql["nmp_app"].update("message_template", {"template_id": template_id}, {"status": 9, "template": json.dumps(template_content)})
        return template_id
    else:
        with allure.step('添加消息模版接口'):
            inputs = {
                "host": env['host']['app_in'],
                "path": add_template_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ''},
                "json": {
                    "channel": channel,
                    "name": template_name,
                    "type": content_type,
                    "template_str": json.dumps(template_content),
                }
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
            template_id = response.get("data")
        with allure.step("发布模板"):
            published_template(env, mysql, template_id)
        return template_id


def init_template(env, mysql, channel, app_id, init_template_map, content_type='text'):
    with allure.step('初始化模版'):
        exist_template_id = {}
        template_name_id_map = {}
        exist_template_map = mysql["nmp_app"].fetch("message_template", {"name in": list(init_template_map.keys()), "channel": channel, "valid": 1, "status": 9}, retry_num=1, )
        for template_map in exist_template_map:
            exist_template_id[template_map.get("name")] = template_map.get("template_id")

        for template_name, template_str in init_template_map.items():
            temp_template_id = exist_template_id.get(template_name)
            if temp_template_id:
                template_name_id_map[template_name] = temp_template_id
            else:
                template_id = create_template_and_published(env, mysql, channel, content_type, template_name, template_str, app_id)
                template_name_id_map[template_name] = template_id
        return template_name_id_map


def init_email_template(env, mysql, app_id=10000, channel="email"):
    """
    R==公共变量
    L==自定义变量
    no_repeat==变量不重复
    repeat == 变量有重复
    part_user == 部分用户有替换值
    part_value == 部分变量有替换值
    "qa_user_name": "http://pangu.nioint.com:5000/pangu/get_user_name",
    "qa_city": "http://pangu.nioint.com:5000/pangu/get_city",
    "qa_part_user": "http://pangu.nioint.com:5000/pangu/get_part_variable",
    "qa_random_str": "http://pangu.nioint.com:5000/pangu/get_variable",
    """
    template_name_id_map = {}
    variable_name_id_map = init_variable(env, mysql)
    cmdopt = env.get("cmdopt")
    qa_user_name_id = variable_name_id_map.get("qa_user_name")
    qa_part_user_id = variable_name_id_map.get("qa_part_user")

    init_template_map = {
        "no_variable": f"【{cmdopt}】正案例_无变量替换的模板",
        "R_no_repeat": f"【{cmdopt}】正案例_只有公共变量模板_变量无重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "R_repeat": f"【{cmdopt}】正案例_只有公共变量模板_变量有重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "L_no_repeat": f"正案例_只有自定义变量模板_变量无重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]",
        "L_repeat": f"【{cmdopt}】正案例_只有自定义变量模板_变量有重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2,
        "L_R_no_repeat": f"【{cmdopt}】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "L_R_repeat": f"【{cmdopt}】正案例_公共变量+自定义变量模板_有重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2 + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "R_part_value": f"【{cmdopt}】反案例_公共变量_部分有对应url" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "R_no_value": f"【{cmdopt}】反案例_公共变量_全部无对应url" + "不存在的公共变量not_exist：[*not_exist*];变量not_exist2：[*not_exist2*]",
        "R_part_user": f"【{cmdopt}】反案例_公共变量_部分用户有对应url" + f"公共变量用户名称qa_part_user：[*{qa_part_user_id}*]",
        "L_part_value": f"【{cmdopt}】反案例_自定义变量_部分字段有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "L_no_value": f"【{cmdopt}】反案例_自定义变量_全部字段无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "L_part_user": f"【{cmdopt}】反案例_自定义变量_部分用户有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "L_no_user": f"【{cmdopt}】反案例_自定义变量_全部用户无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "L_value_R_part_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_part_user：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "L_user_R_part_user": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "L_value_R_no_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + "不存在的公共变量not_exist：[*not_exist*]",
        "R_L_no_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "R_L_part_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "R_L_part_user": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "H5_R_L": H5_R_L,
        "L_R_no_repeat_p_offline": f"【{int(time.time())}】L_R_no_repeat_p_offline【{cmdopt}】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "L_R_no_repeat_p_snapshot": f"【{int(time.time())}】L_R_no_repeat_p_snapshot【{cmdopt}】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "L_R_no_repeat_p_update": f"【{int(time.time())}】L_R_no_repeat_p_update【{cmdopt}】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "L_R_no_repeat_p_delete": f"【{int(time.time())}】L_R_no_repeat_p_delete【{cmdopt}】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "nvwa_policy": nuwa_policy_h5,
    }

    with allure.step('初始化模版'):
        return init_template(env, mysql, channel, app_id, init_template_map, content_type='text')


def init_sms_template(env, mysql, app_id=10000, channel="sms"):
    """
    R==公共变量
    L==自定义变量
    no_repeat==变量不重复
    repeat == 变量有重复
    part_user == 部分用户有替换值
    part_value == 部分变量有替换值
    "qa_user_name": "http://pangu.nioint.com:5000/pangu/get_user_name",
    "qa_city": "http://pangu.nioint.com:5000/pangu/get_city",
    "qa_part_user": "http://pangu.nioint.com:5000/pangu/get_part_variable",
    "qa_random_str": "http://pangu.nioint.com:5000/pangu/get_variable",
    """
    template_name_id_map = {}
    variable_name_id_map = init_variable(env, mysql)
    cmdopt = env.get("cmdopt")
    qa_user_name_id = variable_name_id_map.get("qa_user_name")
    qa_part_user_id = variable_name_id_map.get("qa_part_user")

    init_template_map = {
        "SMS_no_variable": f"【{cmdopt}】正案例_无变量替换的模板",
        "SMS_voice_alarm": f"【{cmdopt}】打电话发短category为alarm,无替换变量",
        "SMS_R_no_repeat": f"【{cmdopt}】正案例_只有公共变量模板_变量无重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_R_repeat": f"【{cmdopt}】正案例_只有公共变量模板_变量有重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "SMS_L_no_repeat": f"【{cmdopt}】正案例_只有自定义变量模板_变量无重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]",
        "SMS_L_repeat": f"【{cmdopt}】正案例_只有自定义变量模板_变量有重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2,
        "SMS_L_R_no_repeat": f"【{cmdopt}】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_L_R_no_repeat_marketing_sms": f"【{cmdopt}_portal_marketing_sms】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_L_R_no_repeat_portal_sms": f"【{cmdopt}_portal_sms】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_L_R_repeat": f"【{cmdopt}】正案例_公共变量+自定义变量模板_有重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2 + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "SMS_R_part_value": f"【{cmdopt}】反案例_公共变量_部分有对应url" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "SMS_R_no_value": f"【{cmdopt}】反案例_公共变量_全部无对应url" + "不存在的公共变量not_exist：[*not_exist*];变量not_exist2：[*not_exist2*]",
        "SMS_R_part_user": f"【{cmdopt}】反案例_公共变量_部分用户有对应url" + f"公共变量用户名称qa_part_user：[*{qa_part_user_id}*]",
        "SMS_L_part_value": f"【{cmdopt}】反案例_自定义变量_部分字段有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "SMS_L_no_value": f"【{cmdopt}】反案例_自定义变量_全部字段无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "SMS_L_part_user": f"【{cmdopt}】反案例_自定义变量_部分用户有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "SMS_L_no_user": f"【{cmdopt}】反案例_自定义变量_全部用户无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "SMS_L_value_R_part_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_part_user：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "SMS_L_user_R_part_user": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_L_value_R_no_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + "不存在的公共变量not_exist：[*not_exist*]",
        "SMS_R_L_no_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_R_L_part_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_R_L_part_user": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
    }
    with allure.step('初始化模版'):
        return init_template(env, mysql, channel, app_id, init_template_map, content_type='text')


def init_sms_voice_template(env, mysql, app_id=10000, channel="voice"):
    """
    R==公共变量
    L==自定义变量
    no_repeat==变量不重复
    repeat == 变量有重复
    part_user == 部分用户有替换值
    part_value == 部分变量有替换值
    "qa_user_name": "http://pangu.nioint.com:5000/pangu/get_user_name",
    "qa_city": "http://pangu.nioint.com:5000/pangu/get_city",
    "qa_part_user": "http://pangu.nioint.com:5000/pangu/get_part_variable",
    "qa_random_str": "http://pangu.nioint.com:5000/pangu/get_variable",
    """
    template_name_id_map = {}
    variable_name_id_map = init_variable(env, mysql)
    cmdopt = env.get("cmdopt")
    qa_user_name_id = variable_name_id_map.get("qa_user_name")
    qa_part_user_id = variable_name_id_map.get("qa_part_user")

    init_template_map = {
        "SMS_voice_no_variable": f"【{cmdopt}】语音环境短信模板,正案例_无变量替换的模板",
        "SMS_voice_alarm_no_variable": f"【{cmdopt}】alarm语音环境短信模板,无替换变量",
        "SMS_voice_R_no_repeat": f"【{cmdopt}】语音环境短信模板,正案例_只有公共变量模板_变量无重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_voice_R_repeat": f"【{cmdopt}】语音环境短信模板,正案例_只有公共变量模板_变量有重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "SMS_voice_L_no_repeat": f"语音环境短信模板,正案例_只有自定义变量模板_变量无重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]",
        "SMS_voice_L_repeat": f"【{cmdopt}】语音环境短信模板,正案例_只有自定义变量模板_变量有重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2,
        "SMS_voice_L_R_no_repeat": f"【{cmdopt}】语音环境短信模板,正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_voice_L_R_repeat": f"【{cmdopt}】语音环境短信模板,正案例_公共变量+自定义变量模板_有重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2 + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "SMS_voice_alarm_L_R_repeat": f"【{cmdopt}】alarm语音环境短信模板,正案例_公共变量+自定义变量模板_有重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2 + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "SMS_voice_R_part_value": f"【{cmdopt}】语音环境短信模板,反案例_公共变量_部分有对应url" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "SMS_voice_R_no_value": f"【{cmdopt}】语音环境短信模板,反案例_公共变量_全部无对应url" + "不存在的公共变量not_exist：[*not_exist*];变量not_exist2：[*not_exist2*]",
        "SMS_voice_R_part_user": f"【{cmdopt}】语音环境短信模板,反案例_公共变量_部分用户有对应url" + f"公共变量用户名称qa_part_user：[*{qa_part_user_id}*]",
        "SMS_voice_L_part_value": f"【{cmdopt}】语音环境短信模板,反案例_自定义变量_部分字段有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "SMS_voice_L_no_value": f"【{cmdopt}】语音环境短信模板,反案例_自定义变量_全部字段无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "SMS_voice_L_part_user": f"【{cmdopt}】语音环境短信模板,反案例_自定义变量_部分用户有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "SMS_voice_L_no_user": f"【{cmdopt}】语音环境短信模板,反案例_自定义变量_全部用户无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "SMS_voice_L_value_R_part_value": f"【{cmdopt}】语音环境短信模板,反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_part_user：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "SMS_voice_L_user_R_part_user": f"【{cmdopt}】语音环境短信模板,反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_voice_L_value_R_no_value": f"【{cmdopt}】v反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + "不存在的公共变量not_exist：[*not_exist*]",
        "SMS_voice_R_L_no_value": f"【{cmdopt}】语音环境短信模板,反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_voice_R_L_part_value": f"【{cmdopt}】语音环境短信模板,反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "SMS_voice_R_L_part_user": f"【{cmdopt}】语音环境短信模板,反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
    }
    with allure.step('初始化模版'):
        return init_template(env, mysql, channel, app_id, init_template_map, content_type='text')


def init_app_template(env, mysql, app_id=10000, channel="app"):
    """
    R==公共变量
    L==自定义变量
    no_repeat==变量不重复
    repeat == 变量有重复
    part_user == 部分用户有替换值
    part_value == 部分变量有替换值
    "qa_user_name": "http://pangu.nioint.com:5000/pangu/get_user_name",
    "qa_city": "http://pangu.nioint.com:5000/pangu/get_city",
    "qa_part_user": "http://pangu.nioint.com:5000/pangu/get_part_variable",
    "qa_random_str": "http://pangu.nioint.com:5000/pangu/get_variable",
    """
    template_name_id_map = {}
    variable_name_id_map = init_variable(env, mysql)
    cmdopt = env.get("cmdopt")
    qa_user_name_id = variable_name_id_map.get("qa_user_name")
    qa_part_user_id = variable_name_id_map.get("qa_part_user")

    init_template_map = {
        "APP_no_variable": f"【{cmdopt}】正案例_无变量替换的模板",
        "APP_R_no_repeat": f"【{cmdopt}】正案例_只有公共变量模板_变量无重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_R_repeat": f"【{cmdopt}】正案例_只有公共变量模板_变量有重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "APP_L_no_repeat": f"正案例_只有自定义变量模板_变量无重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]",
        "APP_L_repeat": f"【{cmdopt}】正案例_只有自定义变量模板_变量有重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2,
        "APP_L_R_no_repeat": f"【{cmdopt}】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_L_R_repeat": f"【{cmdopt}】正案例_公共变量+自定义变量模板_有重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2 + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "APP_R_part_value": f"【{cmdopt}】反案例_公共变量_部分有对应url" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "APP_R_no_value": f"【{cmdopt}】反案例_公共变量_全部无对应url" + "不存在的公共变量not_exist：[*not_exist*];变量not_exist2：[*not_exist2*]",
        "APP_R_part_user": f"【{cmdopt}】反案例_公共变量_部分用户有对应url" + f"公共变量用户名称qa_part_user：[*{qa_part_user_id}*]",
        "APP_L_part_value": f"【{cmdopt}】反案例_自定义变量_部分字段有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "APP_L_no_value": f"【{cmdopt}】反案例_自定义变量_全部字段无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "APP_L_part_user": f"【{cmdopt}】反案例_自定义变量_部分用户有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "APP_L_no_user": f"【{cmdopt}】反案例_自定义变量_全部用户无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "APP_L_value_R_part_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_part_user：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "APP_L_user_R_part_user": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_L_value_R_no_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + "不存在的公共变量not_exist：[*not_exist*]",
        "APP_R_L_no_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_R_L_part_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_R_L_part_user": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_TOB_no_variable": f"【{cmdopt}】正案例_无变量替换的模板",
        "APP_TOB_R_no_repeat": f"【{cmdopt}】正案例_只有公共变量模板_变量无重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_TOB_R_repeat": f"【{cmdopt}】正案例_只有公共变量模板_变量有重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "APP_TOB_L_no_repeat": f"正案例_只有自定义变量模板_变量无重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]",
        "APP_TOB_L_repeat": f"【{cmdopt}】正案例_只有自定义变量模板_变量有重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2,
        "APP_TOB_L_R_no_repeat": f"【{cmdopt}】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_TOB_L_R_repeat": f"【{cmdopt}】正案例_公共变量+自定义变量模板_有重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2 + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "APP_TOB_R_part_value": f"【{cmdopt}】反案例_公共变量_部分有对应url" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "APP_TOB_R_no_value": f"【{cmdopt}】反案例_公共变量_全部无对应url" + "不存在的公共变量not_exist：[*not_exist*];变量not_exist2：[*not_exist2*]",
        "APP_TOB_R_part_user": f"【{cmdopt}】反案例_公共变量_部分用户有对应url" + f"公共变量用户名称qa_part_user：[*{qa_part_user_id}*]",
        "APP_TOB_L_part_value": f"【{cmdopt}】反案例_自定义变量_部分字段有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "APP_TOB_L_no_value": f"【{cmdopt}】反案例_自定义变量_全部字段无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "APP_TOB_L_part_user": f"【{cmdopt}】反案例_自定义变量_部分用户有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "APP_TOB_L_no_user": f"【{cmdopt}】反案例_自定义变量_全部用户无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "APP_TOB_L_value_R_part_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_part_user：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "APP_TOB_L_user_R_part_user": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_TOB_L_value_R_no_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + "不存在的公共变量not_exist：[*not_exist*]",
        "APP_TOB_R_L_no_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_TOB_R_L_part_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "APP_TOB_R_L_part_user": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
    }
    with allure.step('初始化模版'):
        return init_template(env, mysql, channel, app_id, init_template_map, content_type='text')


def init_feishu_template(env, mysql, app_id=10000, channel="feishu"):
    """
    R==公共变量
    L==自定义变量
    no_repeat==变量不重复
    repeat == 变量有重复
    part_user == 部分用户有替换值
    part_value == 部分变量有替换值
    "qa_user_name": "http://pangu.nioint.com:5000/pangu/get_user_name",
    "qa_city": "http://pangu.nioint.com:5000/pangu/get_city",
    "qa_part_user": "http://pangu.nioint.com:5000/pangu/get_part_variable",
    "qa_random_str": "http://pangu.nioint.com:5000/pangu/get_variable",
    """
    template_name_id_map = {}
    variable_name_id_map = init_variable(env, mysql)
    cmdopt = env.get("cmdopt")
    qa_user_name_id = variable_name_id_map.get("qa_user_name")
    qa_part_user_id = variable_name_id_map.get("qa_part_user")

    init_template_map = {
        "FEISHU_no_variable": f"【{cmdopt}】正案例_无变量替换的模板",
        "FEISHU_R_no_repeat": f"【{cmdopt}】正案例_只有公共变量模板_变量无重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "FEISHU_R_repeat": f"【{cmdopt}】正案例_只有公共变量模板_变量有重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "FEISHU_L_no_repeat": f"正案例_只有自定义变量模板_变量无重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]",
        "FEISHU_L_repeat": f"【{cmdopt}】正案例_只有自定义变量模板_变量有重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2,
        "FEISHU_L_R_no_repeat": f"【{cmdopt}】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "FEISHU_L_R_repeat": f"【{cmdopt}】正案例_公共变量+自定义变量模板_有重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2 + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "FEISHU_R_part_value": f"【{cmdopt}】反案例_公共变量_部分有对应url" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "FEISHU_R_no_value": f"【{cmdopt}】反案例_公共变量_全部无对应url" + "不存在的公共变量not_exist：[*not_exist*];变量not_exist2：[*not_exist2*]",
        "FEISHU_R_part_user": f"【{cmdopt}】反案例_公共变量_部分用户有对应url" + f"公共变量用户名称qa_part_user：[*{qa_part_user_id}*]",
        "FEISHU_L_part_value": f"【{cmdopt}】反案例_自定义变量_部分字段有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "FEISHU_L_no_value": f"【{cmdopt}】反案例_自定义变量_全部字段无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "FEISHU_L_part_user": f"【{cmdopt}】反案例_自定义变量_部分用户有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "FEISHU_L_no_user": f"【{cmdopt}】反案例_自定义变量_全部用户无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "FEISHU_L_value_R_part_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_part_user：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "FEISHU_L_user_R_part_user": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "FEISHU_L_value_R_no_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + "不存在的公共变量not_exist：[*not_exist*]",
        "FEISHU_R_L_no_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "FEISHU_R_L_part_value": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "FEISHU_R_L_part_user": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
    }
    with allure.step('初始化模版'):
        return init_template(env, mysql, channel, app_id, init_template_map, content_type='text')


def init_im_template(env, mysql, app_id=10000, channel="im"):
    """
    R==公共变量
    L==自定义变量
    no_repeat==变量不重复
    repeat == 变量有重复
    part_user == 部分用户有替换值
    part_value == 部分变量有替换值
    "qa_user_name": "http://pangu.nioint.com:5000/pangu/get_user_name",
    "qa_city": "http://pangu.nioint.com:5000/pangu/get_city",
    "qa_part_user": "http://pangu.nioint.com:5000/pangu/get_part_variable",
    "qa_random_str": "http://pangu.nioint.com:5000/pangu/get_variable",
    """
    template_name_id_map = {}
    variable_name_id_map = init_variable(env, mysql)
    cmdopt = env.get("cmdopt")
    qa_user_name_id = variable_name_id_map.get("qa_user_name")
    qa_part_user_id = variable_name_id_map.get("qa_part_user")

    init_template_map = {
        "IM_no_variable_V1": f"【{cmdopt}】正案例_无变量替换的模板",
        "IM_R_no_repeat_V1": f"【{cmdopt}】正案例_只有公共变量模板_变量无重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "IM_R_repeat_V1": f"【{cmdopt}】正案例_只有公共变量模板_变量有重复" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "IM_L_no_repeat_V1": f"正案例_只有自定义变量模板_变量无重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]",
        "IM_L_repeat_V1": f"【{cmdopt}】正案例_只有自定义变量模板_变量有重复" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2,
        "IM_L_R_no_repeat_V1": f"【{cmdopt}】正案例_公共变量+自定义变量模板_无重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "IM_L_R_repeat_V1": f"【{cmdopt}】正案例_公共变量+自定义变量模板_有重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2 + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "IM_L_R_repeat_No_From_V1": f"【{cmdopt}】正案例_公共变量+自定义变量模板_有重复变量" + "自定义变量:[#date#]；自定义变量:[#fist_name#]" * 2 + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" * 2,
        "IM_R_part_value_V1": f"【{cmdopt}】反案例_公共变量_部分有对应url" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "IM_R_no_value_V1": f"【{cmdopt}】反案例_公共变量_全部无对应url" + "不存在的公共变量not_exist：[*not_exist*];变量not_exist2：[*not_exist2*]",
        "IM_R_part_user_V1": f"【{cmdopt}】反案例_公共变量_部分用户有对应url" + f"公共变量用户名称qa_part_user：[*{qa_part_user_id}*]",
        "IM_L_part_value_V1": f"【{cmdopt}】反案例_自定义变量_部分字段有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "IM_L_no_value_V1": f"【{cmdopt}】反案例_自定义变量_全部字段无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "IM_L_part_user_V1": f"【{cmdopt}】反案例_自定义变量_部分用户有替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "IM_L_no_user_V1": f"【{cmdopt}】反案例_自定义变量_全部用户无替换" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]",
        "IM_L_value_R_part_value_V1": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_part_user：[*{qa_user_name_id}*]" + "不存在的公共变量not_exist：[*not_exist*]",
        "IM_L_user_R_part_user_V1": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "IM_L_value_R_no_value_V1": f"【{cmdopt}】反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + "不存在的公共变量not_exist：[*not_exist*]",
        "IM_R_L_no_value_V1": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "IM_R_L_part_value_V1": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
        "IM_R_L_part_user_V1": f"【{cmdopt}】反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值" + "自定义变量:[#date#]；变量:[#fist_name#];变量:[#time#]" + f"公共变量用户名称qa_user_name：[*{qa_user_name_id}*]",
    }
    with allure.step('初始化模版'):
        return init_template(env, mysql, channel, app_id, init_template_map, content_type='text')


if __name__ == '__main__':
    create_new_template()
