# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_notify.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/5/13 4:36 下午
# @Description :
"""
   接口文档：http://showdoc.nevint.com/index.php?s=/647&page_id=32691
"""

import json
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.logger import logger as logging

server_app_id = 10000
im_notify_path = "/api/2/in/message/cn/im_notify"
im_notify_eu_path = "/api/2/in/message/eu/im_notify"


class TestNotify(object):
    push_im_notify_keys = "case_name,acc,has_from,msg_body,sync_other_machine,cloud_custom_data,status,num"
    push_im_notify_cases = (
        ["正案例_所有字段有值", True, True, True, 1, True, 1, 1],
        ["正案例_只填必填字段", True, True, True, None, True, None, 1],
        ["正案例_account_ids数量等于100", True, True, True, 1, True, 1,  100],
        ["反案例_account_ids数量大于100", True, True, True, None, None, None, 101],
        ["反案例_account_ids为None", None, True, True, None, None, None, 1],
        ["反案例_from为None", True, False, True, None, None, None, 1],
        ["反案例_msg_body为None", True, True, None, None, None, None, 1],
    )
    push_im_notify_ids = [f"{case[0]}" for case in push_im_notify_cases]

    @pytest.mark.parametrize(push_im_notify_keys, push_im_notify_cases, ids=push_im_notify_ids)
    def test_push_im_notify(self, env, cmdopt, mysql, case_name, acc, has_from, msg_body, sync_other_machine, cloud_custom_data, status, num):
        app_id = 10000
        if cmdopt in ["test", "stg"]:
            target_app_ids = "10001,10002"
        elif cmdopt in ["test_marcopolo", "stg_marcopolo"]:
            target_app_ids = "1000003,1000004"
        if acc:
            user_info_mysql = mysql["nmp_app"].fetch("bindings", where_model={'visible': 1, 'user_id>': 1000, 'app_id in': target_app_ids.split(",")},
                                                     fields=["account_id", "user_id"],
                                                     suffix=f"group by user_id limit {num}")
            account_ids = ",".join([str(u.get("user_id")) for u in user_info_mysql])
        else:
            account_ids = None
        body = {
            'account_ids': account_ids,
            "status": status,
            "cloud_custom_data": str(json.dumps({
                'version': '0.1',
                'platform': 'taitan',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                'business_code': '2.1',
                'function': {
                    'filter': ['nio_cn'],
                    'delete': ['nio_cn']
                }
            })),
            "sync_other_machine": sync_other_machine,
            'msg_body': json.dumps([{
                'MsgType': 'TIMCustomElem',
                'MsgContent': {
                    'Data': str({
                        'major_type': 3,
                        'sub_type': 1,
                        'major': {
                            'title': 'User Service',
                            'status': 1,
                            'text': '${1} order vehicle has been unbound by ${2}',
                            'text_placeholder': [{'start_index': 0, 'length': 4}, {'start_index': 39, 'length': 4}],
                            'buttons': [{'text': 'Check details', 'app_link': 'xxx', 'web_link': 'xxx'}],
                            'ext_data': {},
                            'resource': [
                                {'id': 1, 'highlight': True, 'resource_type': 1, 'account_id': '100662'},
                                {'id': 2, 'highlight': True, 'resource_type': 2, 'text': 'Puyang', 'app_link': 'xxx', 'web_link': 'xxx'},
                                {'id': 3, 'highlight': True, 'resource_type': 3, 'account_id': '100024', 'app_link': 'xxx', 'web_link': 'xxx'}
                            ]
                        }
                    })
                }
            }], ensure_ascii=False)
        }
        if has_from:
            if 'stg' in cmdopt:
                body['from'] = 'SO'
            else:
                body['from'] = 'test'
        if not msg_body:
            body.pop("msg_body")
        if not cloud_custom_data:
            body.pop("cloud_custom_data")
        inputs = {
            "host": env['host']["app_in"],
            "path": im_notify_eu_path if cmdopt in ["test_marcopolo", "stg_marcopolo"] else im_notify_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ''
            },
            "json": body
        }
        response = hreq.request(env, inputs)
        with allure.step(""):
            if "正案例" in case_name:
                assert response['result_code'] == 'success'
                count = 0
                total = len(response['data']['details'])
                for detail in response['data']['details']:
                    if detail['action_status'] == 'OK':
                        count += 1
                logging.info(f'发送成功率{count / total * 100}%')
            else:
                assert response['result_code'] == 'invalid_param'
                if int(num) > 100:
                    assert response['debug_msg'] == 'exceed limit, max receiver is 100'
                else:
                    assert response['debug_msg'] == 'missing account_ids,from or msg_body'
