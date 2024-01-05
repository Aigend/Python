# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author:colin.li
@time: 2021/12/06
@api: POST_/api/2/message_tracker/emay_callback
@showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=32610
@description: This API is offered for Emay to report the sms delivery status
"""
import json

import allure
import time
from utils.http_client import TSPRequest as hreq
from datetime import datetime

from utils.time_parse import now_utc_strtime

emay_push_callback_path = "/api/2/message_tracker/emay_callback"
cn_sms_push_path = "/api/2/in/message/cn/sms_push"


def test_emay_sms_callback(env, mysql, cmdopt):
    app_id = '10000'
    now = datetime.now()
    now_string = now.strftime('%Y-%m-%d %H:%M:%S')
    now_string_for_id = now.strftime('%Y%m%d%H%M%S%f')
    inputs = {
        "host": env['host']['app_in'],
        "path": cn_sms_push_path,
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
            "recipients": env['push_sms']['recipient'],
            "content": f"【{cmdopt}】环境sms push接口推送短信{now_string}",
            "category": 'marketing_sms',
        }
    }
    response = hreq.request(env, inputs)
    assert response['result_code'] == 'success'
    message_id = response['data'].pop('message_id', '')
    time.sleep(10)
    # with allure.step('检查message_state表中对应message_id没有state为27的纪录'):
    #     result = mysql['nmp_app'].fetch('message_state', fields=['state'], where_model={'message_id': message_id})
    #     assert not any(d.get('state', '') == 27 for d in result)

    app_id = 10000
    inputs = {
        "host": env['host']['app_ex'],
        "path": emay_push_callback_path,
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": {
            "reports": json.dumps([{
                "mobile": env['push_sms']['recipient'],
                "smsId": now_string_for_id,
                "customSmsId": message_id,
                "state": "DELIVRD",
                "desc": "成功",
                "receiveTime": now_string,
                "submitTime": now_string,
                "extendedCode": "123"
            }])
        }
    }

    response = hreq.request(env, inputs)
    assert response.get("result_code") == "success"
    time.sleep(10)
    with allure.step('检查message_state表中对应message_id有state为27的纪录'):
        result = mysql['nmp_app'].fetch('message_state', where_model={'message_id': message_id, 'state': 27}, retry_num=80)
        assert result, f"message_id:{message_id} state 27 in mysql is null"
        utc_time = now_utc_strtime()[:13]
        create_time = result[0].get("create_time")[:13]
        assert create_time == utc_time, f"create_time is not utc time, Expect {utc_time} Actual {create_time}"
        update_time = result[0].get("update_time")[:13]
        assert update_time == utc_time, f"update_time is not utc time, Expect {utc_time} Actual {update_time}"