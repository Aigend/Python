# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_reject_config.py
# @Author : qiangwei.zhang
# @time: 2022/01/30
# @api: POST_/api/1/in/message/reject_config
# @showdoc: http://showdoc.nevint.com/index.php?s=/13&page_id=33038
# @Description :脚本描述
"""
参考文档：
开发整理测试重点：https://nio.feishu.cn/docs/doccncraTqCRqvGznLAQ00s48id#rTMDKT
公私网切换逻辑：https://nio.feishu.cn/docs/doccnuBacQdjBFP114kJO0jzYRe
测试case:https://nio.feishu.cn/mindnotes/bmncniH3h1qZxJsn8jTbtIJ2Gmh?appStyle=UI4&domain=www.feishu.cn&locale=zh-CN&refresh=1&tabName=space&theme=light&userId=6955202299270529052#mindmap
压测文档：https://nio.feishu.cn/docs/doccniY2GCKBaEzOyWK7PB1Xpkd?appStyle=UI4&domain=www.feishu.cn&locale=zh-CN&refresh=1&tabName=space&theme=light&userId=6955202299270529052
"""

import allure
import pytest

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.random_tool import random_str

reject_config_path = "/api/1/in/message/reject_config"
random_str100 = ','.join([random_str(32) for i in range(100)])
random_str10 = ','.join([random_str(32) for i in range(10)])
str_repetition = "vid001,vid002,vid003,vid002,vid001"
reject_config_cn_keys = 'case_name,connect_type,vids,port,op'
reject_config_cn_cases = [
    ("正案例_CGW_200083_add_100", 'CGW', random_str10, 20083, "add"),
    ("正案例_CGW_200083_rem_100", 'CGW', random_str10, 20083, "rem"),
    ("正案例_CGW_200083_add_1000", 'CGW', random_str100, 20083, "add"),
    ("正案例_CGW_200083_rem_1000", 'CGW', random_str100, 20083, "rem"),
    ("正案例_CGW_200083_add_包含有重复", 'CGW', f"{random_str(32)}," * 2 + f"{random_str(32)}", 20083, "add"),
    ("正案例_CGW_200083_add100", 'CGW', '74361e94a61846e2a690d2e2a9bf591d', 20083, "add"),
    ("正案例_ADC_200083_add", 'ADC', '74361e94a61846e2a690d2e2a9bf591d', 20083, "add"),
    ("正案例_CGW_200084_add", 'CGW', '74361e94a61846e2a690d2e2a9bf591d', 20084, "add"),
    ("正案例_ADC_200084_add", 'ADC', '74361e94a61846e2a690d2e2a9bf591d', 20084, "add"),
    ("正案例_CGW_200083_rem", 'CGW', '74361e94a61846e2a690d2e2a9bf591d', 20083, "rem"),
    ("正案例_CGW_200084_rem", 'CGW', '74361e94a61846e2a690d2e2a9bf591d', 20084, "rem"),
    ("正案例_ADC_200083_rem", 'ADC', '74361e94a61846e2a690d2e2a9bf591d', 20083, "rem"),
    ("正案例_ADC_200084_rem", 'ADC', '74361e94a61846e2a690d2e2a9bf591d', 20084, "rem"),
]
reject_config_cn_ids = [f"{case[0]}" for case in reject_config_cn_cases]

@pytest.mark.skip("manual")
@pytest.mark.parametrize(reject_config_cn_keys, reject_config_cn_cases, ids=reject_config_cn_ids)
def test_reject_config_cn(env, cmdopt, redis, case_name, connect_type, vids, port, op):
    if cmdopt not in ["test", "stg"]:
        logger.debug(f"该案例只在cn环境执行")
        return 0
    with allure.step("tsp配置mqtt内网连接block名单接口"):
        app_id = 10000
        inputs = {
            "host": env['host']["tsp_in"],
            "path": reject_config_path,
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "data": {
                "vids": vids,
                "type": connect_type,
                "port": port,
                "op": op
            }
        }
        inputs["data"] = {k: v for k, v in inputs["data"].items() if v}
        response = hreq.request(env, inputs)
    with allure.step("tsp配置mqtt内网连接block名单接口"):
        assert response['result_code'] == 'success'
        vid_list = set(vids.split(','))
        assert int(response.get("data")) == len(vid_list)
        for vid in vid_list:
            if op == "add":
                expect_redis_res = True
            else:
                expect_redis_res = False
            redis_res = False
            if connect_type == "CGW":
                redis_res = redis['message'].get_sis_member(f"nmp:reject:CN=TlsLion:{port}", vid)
            elif connect_type == "ADC":
                redis_res = redis['message'].get_sis_member(f"nmp:reject:CN=TlsAsimov:{port}", vid)
            assert expect_redis_res == redis_res


reject_config_cn_negative_keys = 'case_name,connect_type,vids,port,op,expected_res'
reject_config_cn_negative_cases = [
    ("反案例_错误类型_20083_rem", 'CDC', 'fan_an_li_vid', 20083, "rem", {"result_code": "invalid_param", "debug_msg": "type only can be CGW or ADC"}),
    ("反案例_CGW_200083_rem_不存在", 'CGW', random_str(32), 20083, "rem", {"result_code": "success", "data": 0}),
    ("反案例_错误端口_rem", 'ADC', random_str(32), 20085, "add", {"result_code": "success", "data": 1}),
    ("反案例_ADC_20083_错误操作类型", 'ADC', 'fan_an_li_vid', 20085, "error", {"result_code": "invalid_param", "debug_msg": "op only can be add or rem"}),
    # ("反案例_type为None", None, 'fan_an_li_vid', 20083, "rem", "500"),
    ("反案例_vid为None", 'ADC', None, 20083, "rem", {"result_code": "invalid_param", "debug_msg": "require port, vids"}),
    ("反案例_port为None", 'ADC', 'fan_an_li_vid', None, "rem", {"result_code": "invalid_param", "debug_msg": "require port, vids"}),
    # ("反案例_op为None", 'ADC', 'fan_an_li_vid', 20083, None, "500")
]
reject_config_cn_negative_ids = [f"{case[0]}" for case in reject_config_cn_negative_cases]


@pytest.mark.skip("manual")
@pytest.mark.parametrize(reject_config_cn_negative_keys, reject_config_cn_negative_cases, ids=reject_config_cn_negative_ids)
def test_reject_config_negative_cn(env, cmdopt, redis, case_name, connect_type, vids, port, op, expected_res):
    if cmdopt not in ["test", "stg"]:
        logger.debug(f"该案例只在cn环境执行")
        return 0
    with allure.step("tsp配置mqtt内网连接block名单接口"):
        app_id = 10000
        inputs = {
            "host": env['host']["tsp_in"],
            "path": reject_config_path,
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "data": {
                "vids": vids,
                "type": connect_type,
                "port": port,
                "op": op
            }
        }
        inputs["data"] = {k: v for k, v in inputs["data"].items() if v}
        response = hreq.request(env, inputs)
    with allure.step("tsp配置mqtt内网连接block名单接口"):
        response.pop("request_id")
        response.pop("server_time")
        assert_equal(response, expected_res)


vid = "024d9fe2e10fce637f9a6bbe947b1578"
# vid = "ce86a87d33414d38b0820d4fe09358de" # prod
reject_config_stg_cn_keys = 'case_name,connect_type,vids,port,op'
reject_config_stg_cn_cases = [
    ("正案例_CGW_200083_add", 'CGW', vid, 20083, "rem"),
]
reject_config_stg_cn_ids = [f"{case[0]}" for case in reject_config_stg_cn_cases]


@pytest.mark.skip("manual")
@pytest.mark.parametrize(reject_config_stg_cn_keys, reject_config_stg_cn_cases, ids=reject_config_stg_cn_ids)
def test_reject_config_stg_cn(env, cmdopt, redis, case_name, connect_type, vids, port, op):
    if cmdopt not in ["test", "stg"]:
        logger.debug(f"该案例只在cn环境执行")
        return 0
    app_id = 10000
    inputs = {
        "host": env['host']["tsp_in"],
        "path": reject_config_path,
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
        "data": {
            "vids": vids,
            "type": connect_type,
            "port": port,
            "op": op
        }
    }
    inputs["data"] = {k: v for k, v in inputs["data"].items() if v}
    response = hreq.request(env, inputs)
    if "正案例" in case_name:
        assert response['result_code'] == 'success'
        vid_list = set(vids.split(','))
        assert int(response.get("data")) == len(vid_list)
        for vid in vid_list:
            if op == "add":
                expect_redis_res = True
            else:
                expect_redis_res = False
            redis_res = False
            if connect_type == "CGW":
                redis_res = redis['message'].get_sis_member(f"nmp:reject:CN=TlsLion:{port}", vid)
            elif connect_type == "ADC":
                redis_res = redis['message'].get_sis_member(f"nmp:reject:CN=TlsAsimov:{port}", vid)
            assert expect_redis_res == redis_res
