# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_fake_email.py
# @Author : qiangwei.zhang
# @time: 2021/08/19
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述
"""
1.获取申请者票据信息，/acc/3/in/email_ticket/refresh
2.申请假邮箱，/acc/3/in/fake_email/claim
3.根据假邮箱验证码获取，假邮箱票据信息 /acc/2/in/verification_code/email
4.根据票据信息调用注册接口 /acc/3/in/app_email/register

"""

import allure
import pytest
import time
import json
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.random_tool import random_string
from utils.encryption import get_encryption, encrypt, checkedPassword

server_app_id = 10000
fake_email_effect_minutes = 525600  # 假邮箱有效期
fake_email_vc_code_allowed_count = 100000  # 假邮箱验证码可使用次数
claimer_ticket_effect_minutes = 128160  # 申请人票据有效期


def register_change(env, password="pan_gu@123456"):
    key_id, key = get_encryption(env, server_app_id)
    password_e = encrypt(password, key).decode("utf-8")
    return key_id, password_e, password


def email_ticket_refresh(env, mysql, claimer, classifier="fake_email"):
    inputs = {
        "host": env["host"]["app_in"],
        "method": 'POST',
        "path": "/acc/3/in/email_ticket/refresh",
        "params": {
            "app_id": server_app_id,
            "lang": "zh-cn",
            "region": "cn",
            "nonce": random_string(13),
            "sign": ''
        },
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": {
            "email": claimer,
            "effect_minutes": claimer_ticket_effect_minutes,
            "classifier": classifier
        },

    }
    res = hreq.request(env, inputs)
    logger.debug(res)
    db_ticket = mysql["account_center"].fetch('ac_email_ticket', where_model={'email': claimer, 'classifier': classifier}, fields=['ticket'])[0]
    ticket = db_ticket['ticket']
    return claimer, ticket, classifier


def apply_fake_email(env, claimer, ticket):
    inputs = {
        "host": env["host"]["app_in"],
        "path": "/acc/3/in/fake_email/claim",
        "method": "POST",
        "params": {
            "app_id": server_app_id,
            "lang": "zh-cn",
            "region": "eu",
            "nonce": random_string(13),
            "sign": '',
            "hash_type": "sha256"
        },
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": {
            "claimer": claimer,
            "ticket": ticket,
            "effect_minutes": fake_email_effect_minutes,
            "allowed_count": fake_email_vc_code_allowed_count
        }
    }
    res = hreq.request(env, inputs)
    return res


def check_fake_email_verification_code(env, classifier, email, verification_code):
    inputs = {
        "host": env['host']['app_in'],
        "path": "/acc/2/in/verification_code/email",
        "method": "POST",
        "params": {
            "app_id": server_app_id,
            "lang": "zh_cn",
            "region": "cn",
            "nonce": random_string(13),
            "hash_type": "sha256",
            "sign": ''
        },
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "data": {
            "classifier": classifier,
            "email": email,
            "verification_code": verification_code
        }
    }

    r = hreq.request(env, inputs)
    if r['result_code'] == 'success':
        if classifier == 'common_verification':
            return r['result_code']
        else:
            # 从请求结果中获取ticket信息；
            return r['data']['ticket']
    else:
        return r


def fake_email_refresh(env, claimer=None, ticket=None, fake_email=None):
    inputs = {
        "host": env['host']['app_in'],
        "path": "/acc/2/in/verification_code/email",
        "method": "POST",
        "params": {
            "app_id": server_app_id,
            "lang": "zh_cn",
            "region": "cn",
            "nonce": random_string(13),
            "hash_type": "sha256",
            "sign": ''
        },
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "data": {
            "claimer": claimer,
            "ticket": ticket,
            "fake_email": fake_email,
            "effect_minutes": fake_email_effect_minutes,
            "allowed_count": fake_email_vc_code_allowed_count
        }
    }

    res_dict = hreq.request(env, inputs)
    return res_dict


def test_fake_email_register(env, mysql, claimer="qiangwei.zhang@mio.com", password="pan_gu@123456", nick_name=None):
    # 获取随机email,类型不包含‘@nio.com’类型；国内/欧洲服务都不允许‘@nio.com’蔚来邮箱账号注册；
    claimer = "qiangwei.zhang@nio.com"
    classifier = "fake_email"
    cmdopt = env["cmdopt"]
    claimer, ticket, classifier = email_ticket_refresh(env, mysql, claimer, classifier)
    host_app_in = env["host"]["app_in"]
    host_app_ex = env["host"]["app_ex"]
    logger.debug(f"用户注册设置的明码password是：{password}，长度是:{len(password)}")
    # 获取注册email账号需要的ticket;
    fake_email_res = apply_fake_email(env, claimer, ticket)
    fake_email = fake_email_res.get("data").get("fake_email")
    verification_code = fake_email_res.get("data").get("verification_code")
    # 获取注册email账号需要的ticket;
    register_classifier = "register"
    ticket = check_fake_email_verification_code(env, register_classifier, fake_email, verification_code)
    key_id, password_e, password = register_change(env, password)
    if isinstance(ticket, dict):
        return ticket
    if not nick_name:
        nick_name = f"QA_RM_{random_string(10)}"
    inputs = {
        "host": host_app_in,
        "path": "/acc/3/in/app_email/register",
        "method": "POST",
        "params": {
            "app_id": server_app_id,
            "lang": "zh-cn",
            "region": "eu",
            "hash_type": "sha256",
            "nonce": random_string(13),
            "sign": ''
        },
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": {
            "origin_app_id": server_app_id,
            "email": fake_email,
            "ticket": ticket,
            "key_id": key_id,
            "password_e": password_e,
            "nick_name": nick_name,
            "device_id": "amodnwien",
            "terminal": json.dumps({"name": "我的华为手机", "model": "HUAWEI P10"}),
            "ip": "192.2.3.4",
            "login_flag": "true"
        }
    }
    res_dict = hreq.request(env, inputs)
    if res_dict.get("result_code") == "success":
        fake_email_info = {
            "email": fake_email,
            "verification_code": verification_code,
            "helpful_hints": f"【{cmdopt}】环境假邮箱账号有效期:{int(fake_email_effect_minutes / 60 / 24)}天,验证码可用次数:{fake_email_vc_code_allowed_count}次",
        }
        res_dict["fake_email_info"] = fake_email_info
        logger.debug(res_dict)
        return res_dict
    else:
        logger.debug(res_dict)
        return res_dict
