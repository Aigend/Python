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
from utils.time_parse import now_utc_strtime

hw_push_callback_path = "/api/2/message_tracker/hw_cb"
app_notify_path = "/api/2/in/message/app_notify"


@pytest.mark.parametrize('category, channel, host_key, data_key',
                         [
                             ('activity', 'hwpush', "app_in", "nmp_app"),
                         ])
def test_hw_push_callback(env, mysql, cmdopt, category, channel, host_key, data_key, ):
    num = 10
    brand = 'Huawei'
    if cmdopt in ["test", "stg"]:
        target_app_ids = "10001,10002"
        push_app_id = 10001  # cn环境安卓app_id 
    elif cmdopt in ["test_marcopolo", "stg_marcopolo"]:
        target_app_ids = "1000003,1000004"
        push_app_id = 1000004  # eu环境安卓app_id
    sql = f"select b.`user_id` as user_id,b.client_id as client_id,c.device_token  as device_token from clients c,bindings b where c.client_id= b.client_id and b.visible = 1 and c.brand = '{brand}' and c.app_id ={push_app_id} and c.`device_token` is not NULL limit {num}"
    user_infos = mysql['nmp_app'].fetch_by_sql(sql)
    user_ids = ""
    device_tokens = []
    app_id = 10000
    for uid in user_infos:
        device_tokens.append(f"{uid.get('device_token')}")
        if not user_ids:
            user_ids = str(uid.get("user_id"))
        else:
            user_ids = user_ids + "," + str(uid.get("user_id"))
    http = {
        "host": env['host'][host_key],
        "path": "/api/2/in/message/app_notify",
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
            'account_ids': user_ids,
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
                "title": f"【{cmdopt}】环境{channel}渠道推送测试"
            })
        },
    }
    response = hreq.request(env, http)
    assert response['result_code'] == 'success'
    message_id = response['data'].pop('message_id', '')
    time.sleep(10)
    hw_statuses = []
    for token in device_tokens:
        tmp_status = {"biTag": f"{message_id}", "appid": "0000000013", "status": 0, "timestamp": int(time.time() * 1000), "requestId": "1234567890", "token": token}
        hw_statuses.append(tmp_status)
    app_id = 10000
    inputs = {
        "host": env['host']['app_ex'],
        "path": hw_push_callback_path,
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "params": {"hash_type": "sha256", "app_id": app_id, "nonce": str(time.time()), "sign": ""},
        "json": {"statuses": hw_statuses}
    }
    response = hreq.request(env, inputs)
    assert response.get("result_code") == "success"
    get_client_by_token_sql = f"SELECT c.client_id as client_id  FROM clients  AS c LEFT JOIN bindings AS b ON c.id = b.cidx WHERE c.visible=true AND Ifnull(`b`.`visible`,true)=true AND device_token IN {tuple(device_tokens)} GROUP BY device_token HAVING max(c.update_time)"
    clients = mysql['nmp_app'].fetch_by_sql(get_client_by_token_sql)
    res = mysql['nmp_app'].fetch("message_state", {"message_id": message_id}, retry_num=70)
    utc_time = now_utc_strtime()[:13]
    create_time = res[0].get("create_time")[:13]
    assert create_time == utc_time, f"create_time is not utc time, Expect {utc_time} Actual {create_time}"
    update_time = res[0].get("update_time")[:13]
    assert update_time == utc_time, f"update_time is not utc time, Expect {utc_time} Actual {update_time}"
    error_client = []
    for client in clients:
        res = mysql['nmp_app'].fetch("message_state", {"client_id": client.get('client_id'), "message_id": message_id, "state": 27}, retry_num=70)
        if not res:
            error_client.append(client.get('client_id'))
        logger.debug(res)
    logger.debug(error_client)
    assert len(error_client) == 0
