# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : conftest.py
# @Author : qiangwei.zhang
# @time: 2021/12/31
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述
import pytest

from utils.validation_data_format import validation_e164_mobile, validation_fake_mobile, validation_cn_fake_mobile


def generate_sms_result(recipients):
    expect_details = []
    failure_num, success_num = 0, 0
    for mobile in recipients.split(","):
        tmp_dict = {
            "recipient": mobile,
        }
        if validation_fake_mobile(mobile) or validation_cn_fake_mobile(mobile):
            tmp_dict["result"] = "success"
            tmp_dict["reason"] = "mobile is fake, will not send sms"
            success_num += 1
            expect_details.append(tmp_dict)
            continue
        if not validation_e164_mobile(mobile):
            tmp_dict["result"] = "invalid_recipient"
            tmp_dict["reason"] = "mobile numbers must follow E.164, will not send sms"
            failure_num += 1
            expect_details.append(tmp_dict)
            continue
        tmp_dict["result"] = "success"
        success_num += 1
        expect_details.append(tmp_dict)
    expected_res = {
        "data": {
            "details": expect_details,
            "success": success_num,
            "failure": failure_num,
        },
        "result_code": "success",
    }
    return expected_res


def generate_sms_success(recipients):
    expect_details = []
    failure_num, success_num = 0, 0
    for mobile in recipients.split(","):
        tmp_dict = {"recipient": mobile, "result": "success"}
        success_num += 1
        expect_details.append(tmp_dict)
    expected_res = {
        "data": {
            "details": expect_details,
            "success": success_num,
            "failure": failure_num,
        },
        "result_code": "success",
    }
    return expected_res


def generate_voice_sms_result(recipients):
    expect_details = []
    failure_num, success_num = 0, 0
    for mobile in recipients.split(","):
        tmp_dict = {
            "recipient": mobile,
        }
        if validation_fake_mobile(mobile) or validation_cn_fake_mobile(mobile):
            tmp_dict["result"] = "error"
            tmp_dict["reason"] = "mobile is fake, will not send sms"
            failure_num += 1
            expect_details.append(tmp_dict)
            continue
        if not validation_e164_mobile(mobile):
            tmp_dict["result"] = "invalid_recipient"
            tmp_dict["reason"] = "phone number should follow E.164 stander, will not send sms"
            failure_num += 1
            expect_details.append(tmp_dict)
            continue
        tmp_dict["result"] = "success"
        success_num += 1
        expect_details.append(tmp_dict)
    expected_res = {
        "data": {
            "details": expect_details,
            "success": success_num,
            "failure": failure_num,
        },
        "result_code": "success",
    }
    return expected_res


def generate_emay_sms_result(recipients):
    expect_details = []
    failure_num, success_num = 0, 0
    for mobile in recipients.split(","):
        tmp_dict = {
            "recipient": mobile,
        }
        if validation_fake_mobile(mobile):
            tmp_dict["result"] = "error"
            tmp_dict["reason"] = "mobile is fake, will not send sms"
            failure_num += 1
            expect_details.append(tmp_dict)
            continue
        if not validation_e164_mobile(mobile):
            tmp_dict["result"] = "invalid_recipient"
            tmp_dict["reason"] = "mobile numbers must follow E.164, will not send sms"
            failure_num += 1
            expect_details.append(tmp_dict)
            continue
        tmp_dict["result"] = "success"
        success_num += 1
        expect_details.append(tmp_dict)
    expected_res = {
        "data": {
            "details": expect_details,
            "success": success_num,
            "failure": failure_num,
        },
        "result_code": "success",
    }
    return expected_res


sms_path = [
    "/api/2/in/message/cn/sms_push",
    "/api/2/in/message/cn/sms_direct_push",
]


@pytest.fixture(scope='class', autouse=False, params=sms_path)
def get_sms_path(request):
    yield request.param
