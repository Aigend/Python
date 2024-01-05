# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_sms.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/3/23 11:02 上午
# @Description :
import time

import allure
import pytest

from config.settings import BASE_DIR
from tests.app_message_center.clear_rate_limit import clear_rate_limit
from tests.app_message_center.conftest import generate_sms_result, generate_emay_sms_result, generate_sms_success
from tests.app_message_center.test_data.mobile_phone_number_prefix import prefixSorted
from utils.http_client import TSPRequest as hreq
from utils.collection_message_states import collection_message_states
from utils.logger import logger
from utils.assertions import assert_equal
from utils.random_tool import random_cn_string, random_string
from utils.random_tool import random_int
from utils.time_parse import now_shanghai_strtime

norway_phone_number = [
    ("+4795861510", "Vijay Sharma", "vijay.sharma@nio.com"),
    ("+4746821625", "Espen Byrjall", "espen.byrjall@nio.com"),
    ("+4790416210", "Jangir", "jangir.taher@nio.com"),
    ("+4792256265", "Stine Skyseth", "stine.skyseth@nio.com"),
    ("+4748361533", "Ola Smines", "ola.smines@nio.com"),
    ("+4745243903", "Jon Christian Aardal", "jonchristian.aardal@nio.com"),
    ("+4791305149", "Marianne Moelmen", "marianne.moelmen@nio.com"),
    ("+4790551411", "Marius Hayler", "marius.hayler@nio.com"),
    ("+4746895930", "Renate Eliesen", "renate.eliesen1@nio.com"),
]
skip_env_list = ["test_marcopolo", "stg_marcopolo"]
cn_sms_Emay_push_path = "/api/2/in/message/cn/marketing_sms_push"
app_id = 10001
recipient_one_real = "+8617610551933"
recipient_empty = ""
recipient_one_empty_number = "+86170000000000"
recipient_one_invalid = "99904060800000"
recipient_one_invalid1 = "+9990406080000012212122112122121"

recipients_n2 = "+8617610551933,+8613691178976"
recipients_n1_e2 = "+8617610551933,9987863464,cuereddss"
recipients_n0_e3 = "97610551933,83691178976,9987863464,"
recipients_n3_c1 = "+8617610551933,+8613691178976,+8617610551933"

random_list = [f"+86{random_int(12)}" for i in range(1000)]
recipients_1000 = ",".join(random_list)


@pytest.mark.run(order=1)
class TestPushSMS(object):
    """
    接口文档 http://showdoc.nevint.com/index.php?s=/647&page_id=32390
    """
    push_sms_emay_cn_keys = "case_name,recipients,content,content_type,content_length,category,host_key,data_key,send_time"
    push_sms_emay_cn_cases = [
        # ("正案例_单个正常_英文1000字以内", recipient_one_real, "content", "English", 500, "marketing_sms", "app_in", "nmp_app",None),
        # ("正案例_单个正常_英文1000字", recipient_one_real, "content", "English", 1000, "marketing_sms", "app_in", "nmp_app",None),
        # ("正案例_单个正常_英文超过1000字", recipient_one_real, "content", "English", 3000, "marketing_sms", "app_in", "nmp_app",None),
        # ("正案例_单个正常_中文500字以内", recipient_one_real, "content", "Chinese", 100, "marketing_sms", "app_in", "nmp_app", None),
        # ("反案例_单个正常_5分钟前", recipient_one_real, "content", "Chinese", 100, "marketing_sms", "app_in", "nmp_app", now_shanghai_strtime(offset_sec=-60*5)),
        # ("反案例_单个正常_当前时间", recipient_one_real, "content", "Chinese", 100, "marketing_sms", "app_in", "nmp_app", now_shanghai_strtime(offset_sec=0)),
        # ("正案例_单个正常_1分钟后", recipient_one_real, "content", "Chinese", 100, "marketing_sms", "app_in", "nmp_app", now_shanghai_strtime(offset_sec=60)),
        # ("正案例_单个正常_5分钟后", recipient_one_real, "content", "Chinese", 100, "marketing_sms", "app_in", "nmp_app", now_shanghai_strtime(offset_sec=60 * 5)),
        # ("正案例_单个正常_10分钟后", recipient_one_real, "content", "Chinese", 100, "marketing_sms", "app_in", "nmp_app", now_shanghai_strtime(offset_sec=60*10+5)),
        # ("正案例_单个正常_5天后", recipient_one_real, "content", "Chinese", 100, "marketing_sms", "app_in", "nmp_app", now_shanghai_strtime(offset_sec=60*60*24*5)),
        # ("正案例_单个正常_50天后", recipient_one_real, "content", "Chinese", 100, "marketing_sms", "app_in", "nmp_app", now_shanghai_strtime(offset_sec=60*60*24*50)),
        # ("反案例_错误时间格式大于24点", recipient_one_real, "content", "Chinese", 100, "marketing_sms", "app_in", "nmp_app", "2021-11-18 39:22:06"),
        # ("反案例_错误时间格式int", recipient_one_real, "content", "Chinese", 100, "marketing_sms", "app_in", "nmp_app", int(time.time())),
        ("正案例_单个正常_中文20字", recipient_one_real, "content", "Chinese", 20, "ads", "app_in", "nmp_app", None),
        # ("正案例_单个正常_中文500字", recipient_one_real, "content", "Chinese", 500, "ads", "app_in", "nmp_app",None),
        # ("正案例_单个正常_大于中文500字", recipient_one_real, "content", "Chinese", 800, "ads", "app_in", "nmp_app",None),
        # ("正案例_单个空号", recipient_one_empty_number, "content", "Chinese", 100, "ads", "app_in", "nmp_app",None),
        # ("反案例_单个不符合规范_", recipient_one_invalid, "content", "Chinese", 100, "ads", "app_in", "nmp_app",None),
        # ("反案例_单个不符合规范_长度过大", recipient_one_invalid1, "content", "Chinese", 100, "ads", "app_in", "nmp_app",None),
        # ("反案例_单个不传recipients", None, "content", "Chinese", 100, "ads", "app_in", "nmp_app",None),
        # ("反案例_单个recipients为空", recipient_empty, "content", "Chinese", 100, "ads", "app_in", "nmp_app",None),
        # ("反案例_单个不传content", recipient_one_real, None, "Chinese", 100, "ads", "app_in", "nmp_app",None),
        # ("反案例_单个content内容为空", recipient_one_real, "content", "Chinese", 0, "ads", "app_in", "nmp_app",None),
        # ("正案例_单个不传category", recipient_one_real, "content", "Chinese", 100, None, "app_in", "nmp_app",None),
        # #多个
        # ("正案例_多个正常无重复", recipients_n2, "content", "Chinese", 100, None, "app_in", "nmp_app",None),
        # ("正案例_多个部分异常", recipients_n1_e2, "content", "Chinese", 100, None, "app_in", "nmp_app",None),
        # ("反案例_多个全部异常", recipients_n0_e3, "content", "Chinese", 100, None, "app_in", "nmp_app",None),
        # ("正案例_多个有重复", recipients_n3_c1, "content", "Chinese", 100, None, "app_in", "nmp_app",None),
        # ("正案例_1000个", recipients_1000, "content", "Chinese", 100, None, "app_in", "nmp_app", None),
    ]
    push_sms_emay_cn_ids = [f"{case[0]}" for case in push_sms_emay_cn_cases]

    @pytest.mark.parametrize(push_sms_emay_cn_keys, push_sms_emay_cn_cases, ids=push_sms_emay_cn_ids)
    def test_push_sms_emay_cn(self, env, cmdopt, mysql, case_name, recipients, content, content_type, content_length, category, host_key, data_key, send_time):
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        content_str = random_cn_string(content_length)
        if content_type == "English":
            content_str = random_string(content_length)
        inputs = {
            "host": env['host'][host_key],
            "path": cn_sms_Emay_push_path,
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
                "recipients": recipients,
                "content": f"【{cmdopt}_center_marketing_sms】create_time{now_shanghai_strtime()},send_time:{send_time}{content_length}{content_str}" if content_length > 0 else "",
                "category": category,
            }
        }
        if not content:
            inputs.get("json").pop("content")
        if not category:
            inputs.get("json").pop("category")
        if not recipients:
            inputs.get("json").pop("recipients")
        if send_time:
            inputs["json"]["send_time"] = send_time
        response = hreq.request(env, inputs)
        if case_name.startswith("正案例"):
            assert response['result_code'] == 'success'
            message_id = response['data']['message_id']
            for recipient in recipients.split(','):
                if "+" not in recipient:
                    break
                sms_history = mysql[data_key].fetch("sms_history", {"message_id": message_id, "recipient": recipient}, ["recipient"], retry_num=10)
                assert sms_history
                sms_history_info = mysql[data_key].fetch("sms_history_meta_info", {"message_id": message_id}, retry_num=10)
                assert len(sms_history_info) == 1
                # 本次查询是为了确保所有状态已入库,27状态是回调结果有一定延后
                mysql[data_key].fetch("message_state", {"message_id": message_id, "state": 27}, ["state"], retry_num=150)
                message_state = mysql[data_key].fetch("message_state", {"message_id": message_id}, ["state"])
                expected_value = [{'state': 21}, {'state': 22}, {'state': 25}, {'state': 26}, {'state': 27}]
                message_state_sorted = sorted(message_state, key=lambda x: x["state"])
                expected_value_sorted = sorted(expected_value, key=lambda x: x["state"])
                assert_equal(message_state_sorted, expected_value_sorted)
        else:
            assert response['result_code'] == 'invalid_param'

    push_emay_sms_cn_negative_keys = "case_name,user_key,recipient,content,category,host_key,data_key"
    push_emay_sms_cn_negative_cases = [
        ("反案例_content为None", "recipient", "+8617610551933", None, "ads", "app_in", "nmp_app"),
        ("反案例_category为None", "recipient", "+8617610551933", "content", None, "app_in", "nmp_app"),
        ("反案例_recipient为None", "recipient", None, "content", None, "app_in", "nmp_app"),
        ("反案例_account_id为None", "account_id", None, "content", None, "app_in", "nmp_app"),
        ("反案例_user_id为None", "user_id", None, "content", None, "app_in", "nmp_app"),
        ("反案例_all_invalid_recipient", "recipient", "+86 17610551933,17610551933,we2321113,98761761234,+8698761761234", "content", "ads", "app_in", "nmp_app"),
        ("反案例_部分invalid_recipient", "recipient", "+8617610551933,+86 17610551933", "content", "ads", "app_in", "nmp_app"),
    ]
    push_emay_sms_cn_negative_ids = [f"{case[0]}" for case in push_emay_sms_cn_negative_cases]

    @pytest.mark.parametrize(push_emay_sms_cn_negative_keys, push_emay_sms_cn_negative_cases, ids=push_emay_sms_cn_negative_ids)
    def test_push_emay_sms_negative_case(self, env, cmdopt, redis, case_name, user_key, recipient, content, category, host_key, data_key):
        clear_rate_limit(redis, cmdopt, app_id)
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        inputs = {
            "host": env['host'][host_key],
            "path": cn_sms_Emay_push_path,
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
                f"{user_key}s": recipient,
                "content": f"【{cmdopt}】环境sms push接口推送短信{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}{case_name}",
                "category": category,
            }
        }
        if not content:
            inputs.get("json").pop("content")
        if not category:
            inputs.get("json").pop("category")
        response = hreq.request(env, inputs)
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        if response.get("result_code") == "success":
            response.pop("request_id")
            response.pop("server_time")
            response["data"].pop("message_id")
            expected_res = generate_sms_result(recipient)
            expected_res["data"]["details"] = sorted(expected_res["data"]["details"], key=lambda x: x['recipient'])
            response["data"]["details"] = sorted(response["data"]["details"], key=lambda x: x['recipient'])
            assert_equal(response, expected_res)
        else:
            response.pop("request_id")
            response.pop("server_time")
            expected_res = {"result_code": "invalid_param", "debug_msg": "Recipients or content is empty"}
            assert_equal(response, expected_res)

    # push_emay_sms_cn_country_code_keys = "country_name,prefix"
    # push_emay_sms_cn_country_code_cases = [(cc.get("cn"), cc.get("prefix")) for cc in prefixSorted]
    # push_emay_sms_cn_country_code_ids = [f"{case[0]}_{case[1]}" for case in push_emay_sms_cn_country_code_cases]
    #
    # @pytest.mark.skip("manual")
    # @pytest.mark.parametrize(push_emay_sms_cn_country_code_keys, push_emay_sms_cn_country_code_cases, ids=push_emay_sms_cn_country_code_ids)
    # def push_emay_sms_country_code_case(self, env, cmdopt, redis, country_name, prefix):
    #     if cmdopt in skip_env_list:
    #         logger.debug(f"该测试案例不适用【{cmdopt}】环境")
    #         return 0
    #     recipient = f"{prefix}{random_int(8)}"
    #     inputs = {
    #         "host": env['host']["app_in"],
    #         "path": cn_sms_Emay_push_path,
    #         "method": "POST",
    #         "headers": {"Content-Type": "application/json"},
    #         "params": {
    #             "region": "cn",
    #             "lang": "zh-cn",
    #             "hash_type": "sha256",
    #             "app_id": app_id,
    #             "sign": ""
    #         },
    #         "json": {
    #             f"recipients": recipient,
    #             "content": f"【{cmdopt}】环境sms push接口推送短信{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}{country_name}",
    #             "category": "notification",
    #         }
    #     }
    #     response = hreq.request(env, inputs)
    #     with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
    #         if "test" in cmdopt:
    #             redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
    #     if response.get("result_code") == "success":
    #         response.pop("request_id")
    #         response.pop("server_time")
    #         response["data"].pop("message_id")
    #         expected_res = generate_sms_success(recipient)
    #         expected_res["data"]["details"] = sorted(expected_res["data"]["details"], key=lambda x: x['recipient'])
    #         response["data"]["details"] = sorted(response["data"]["details"], key=lambda x: x['recipient'])
    #         assert_equal(response, expected_res)

    push_emay_sms_cn_foreign_keys = "case_name,user_name,recipient,host_key,data_key"
    push_emay_sms_cn_foreign_cases = [
        ("正案例_国外手机号挪威", "Vijay Sharma", "+4795861510", "app_in", "nmp_app"),
        # "+4746895930", "Renate Eliesen"
        # ("正案例_国外手机号挪威", "Renate Eliesen", "+4746895930", "app_in", "nmp_app"),
    ]
    push_emay_sms_cn_foreign_ids = [f"{case[0]}" for case in push_emay_sms_cn_foreign_cases]

    @pytest.mark.skip("manual")
    @pytest.mark.parametrize(push_emay_sms_cn_foreign_keys, push_emay_sms_cn_foreign_cases, ids=push_emay_sms_cn_foreign_ids)
    def test_push_emay_sms_foreign_case(self, env, cmdopt, redis, case_name, user_name, recipient, host_key, data_key):
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        inputs = {
            "host": env['host'][host_key],
            "path": cn_sms_Emay_push_path,
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
                "recipients": recipient,
                "content": f"Hi {user_name} NIO emay messages to test if any bother please forgive me, Best wishes for you",
                "category": "notification",
            }
        }
        response = hreq.request(env, inputs)
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        if response.get("result_code") == "success":
            response.pop("request_id")
            response.pop("server_time")
            response["data"].pop("message_id")
            expected_res = generate_sms_result(recipient)
            expected_res["data"]["details"] = sorted(expected_res["data"]["details"], key=lambda x: x['recipient'])
            response["data"]["details"] = sorted(response["data"]["details"], key=lambda x: x['recipient'])
            assert_equal(response, expected_res)


def user_exist_uds(env, recipient):
    app_id = 10001
    host = env["host"]["uds_in"]
    inputs = {
        "host": host,
        "path": "/uds/in/user/v2/users",
        "method": "GET",
        "params": {
            "hash_type": "sha256",
            "app_id": app_id,
            "mobile": recipient,
            "sign": ""
        }
    }
    response = hreq.request(env, inputs)
    assert response['result_code'] == 'success'


def emay_data():
    for i in range(1):
        random_list = [f"+86{str(random_int(12))}" for i in range(1000)]
        recipients_1000 = ",".join(random_list)
        file_path = f'{BASE_DIR}/data/app_message_center_emay_recipient_14.txt'
        with open(file_path, "a", encoding="utf-8") as e_f:
            e_f.write(f"{recipients_1000}\n")
