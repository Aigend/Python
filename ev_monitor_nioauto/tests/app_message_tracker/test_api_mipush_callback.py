# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_mipush_callback.py
# @Author : qiangwei.zhang
# @time: 2021/09/10
# @api: GET_/api/XXX 【必填】
# @showdoc:http://showdoc.nevint.com/index.php?s=/13&page_id=1273
# @Description :脚本描述

import allure
import pytest
import time
import json
from utils.http_client import TSPRequest as hreq
from utils.logger import logger

# i_push_callback_path = "/api/2/message/m_cb"
from utils.time_parse import now_utc_strtime

app_notify_path = "/api/1/in/message/notify"


@pytest.mark.parametrize('category, channel, host_key, data_key',
                         [
                             ('activity', 'mipush', "app_in", "nmp_app"),
                         ])
def test_api_mi_push_callback(env, mysql, cmdopt, category, channel, host_key, data_key, ):
    num = 10
    brand = 'xiaomi'
    if cmdopt in ["test", "stg"]:
        target_app_ids = "10001,10002"
        push_app_id = 10001
    elif cmdopt in ["test_marcopolo", "stg_marcopolo"]:
        target_app_ids = "1000003,1000004"
        push_app_id = 1000004
    else:
        assert False
    sql = f"select b.`user_id` as user_id,b.client_id as client_id,c.device_token  as device_token from clients c,bindings b where c.client_id= b.client_id and b.visible = 1 and c.brand = '{brand}' and c.app_id ={push_app_id} and c.`device_token`   is not NULL limit {num}"
    user_infos = mysql['nmp_app'].fetch_by_sql(sql)
    user_ids = ""
    client_ids, device_tokens = [], []
    app_id = 10000
    for uid in user_infos:
        device_tokens.append(f"{uid.get('device_token')}")
        client_ids.append(f"{uid.get('client_id')}")
        if not user_ids:
            user_ids = str(uid.get("user_id"))
        else:
            user_ids = user_ids + "," + str(uid.get("user_id"))
    http = {
        "host": env['host'][host_key],
        "path": app_notify_path,
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "params": {
            "region": "cn",
            "lang": "zh-cn",
            "hash_type": "sha256",
            "app_id": app_id,
            "sign": ''
        },
        "data": {
            'nonce': 'MrVIRwkCLBKySgCA',
            'user_ids': user_ids,
            # 'user_ids': env['nmp_app']['push_notify']['user1']['account_id'],
            'ttl': 100000,
            'target_app_ids': target_app_ids,
            'do_push': True,
            'scenario': 'ls_link',
            'channel': channel,
            "category": category,
            "pass_through": 0,
            "store_history": True,
            'payload': json.dumps({
                "target_link": "http://www.niohome.com",
                "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} category:{category}",
                "title": f"【{cmdopt}】环境{channel} 测试mipush回调"
            })
        },
    }
    response = hreq.request(env, http)
    assert response['result_code'] == 'success'
    message_id = response['data'].pop('message_id', '')
    time.sleep(10)
    with allure.step('检查message_state表中对应message_id有state为27的纪录'):
        result = mysql['nmp_app'].fetch('message_state', where_model={'message_id': message_id}, retry_num=80)
        utc_time = now_utc_strtime()[:13]
        create_time = result[0].get("create_time")[:13]
        assert create_time == utc_time, f"create_time is not utc time, Expect {utc_time} Actual {create_time}"
        update_time = result[0].get("update_time")[:13]
        assert update_time == utc_time, f"update_time is not utc time, Expect {utc_time} Actual {update_time}"
        result_state_27 = mysql['nmp_app'].fetch('message_state', where_model={'message_id': message_id, 'state': 27}, retry_num=80)
        assert result_state_27
