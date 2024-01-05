"""
   接口文档：http://showdoc.nevint.com/index.php?s=/647&page_id=33748
   消息格式文档：https://cloud.tencent.com/document/product/269/2720
   自动化测试只涵盖了文本消息，地理位置消息，表情消息和自定义信息，剩余的语音信息，图像信息，文件信息和视频信息因为需要引入额外文件同时对信息平台来说处理没有区别，所以暂时未引入自动化
"""

import json
from datetime import datetime

import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.logger import logger

server_app_id = 10000
im_notify_path = "/api/2/in/message/cn/im_notify_by_account"


class TestNotify(object):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    push_im_notify_keys = "case_name,msg_type,msg_content,num"
    push_im_notify_cases = (
        ["正案例_文本消息", 'TIMTextElem', {'Text': f'[{now}] 测试文本'}, 1],
        ["正案例_自定义消息", 'TIMCustomElem', {
            'Data': json.dumps({
                'type': 5,
                'content': {
                    'invite_id': '2527',
                    'title': 'qwerqwe invite u to enter group',
                    'content': f'[{now}] aaa invite u to enter group,please check!',
                    'image_url': ''
                }
            })
        }, 1],
        ["正案例_account_ids数量等于100", 'TIMTextElem', {'Text': f'[{now}] 测试文本'}, 100],
        ["反案例_account_ids数量大于100", 'TIMTextElem', {'Text': f'[{now}] 测试文本'}, 101],
        ["反案例_msg_body为None", 'TIMTextElem', None, 1],
    )
    push_im_notify_ids = [f"{case[0]}" for case in push_im_notify_cases]

    @pytest.mark.parametrize(push_im_notify_keys, push_im_notify_cases, ids=push_im_notify_ids)
    def test_push_im_notify(self, env, cmdopt, mysql, case_name, msg_type, msg_content, num):
        if cmdopt not in ["test", "stg"]:
            logger.debug(f"该案例只在cn环境执行")
            return 0
        app_id = 10000
        target_app_ids = "10001,10002"
        user_info_mysql = mysql["nmp_app"].fetch("bindings", where_model={'visible': 1, 'user_id>': 1000,
                                                                          'app_id in': target_app_ids.split(",")},
                                                 fields=["account_id", "user_id"],
                                                 suffix=f"group by user_id limit {num + 1}")
        sender = user_info_mysql.pop()['user_id']
        account_ids = ",".join([str(u.get("user_id")) for u in user_info_mysql])
        inputs = {
            "host": env['host']["app_in"],
            "path": im_notify_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ''
            },
            "json": {
                'account_ids': account_ids,
                'from': sender,
                "sync_other_machine": 2,
                'msg_body': json.dumps([{
                    'MsgType': 'TIMTextElem',
                    'MsgContent': msg_content
                }])
            },
        }
        if not msg_content:
            inputs["json"].pop("msg_body")
        response = hreq.request(env, inputs)
        with allure.step(""):
            if "正案例" in case_name:
                assert response['result_code'] == 'success'
            else:
                assert response['result_code'] == 'invalid_param'
                if int(num) > 100:
                    assert response['debug_msg'] == 'exceed limit, max receiver is 100'
                else:
                    assert response['debug_msg'] == 'Invalid param, from or account_ids or msg_body is empty.'
