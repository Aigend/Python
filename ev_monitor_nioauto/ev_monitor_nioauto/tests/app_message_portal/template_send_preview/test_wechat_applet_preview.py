# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2022/05/17
@api: POST_/api/2/in/message_portal/template/cn/wechat_applet/preview
@showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=33914
@description: 微信小程序模版preview
我们使用业务方提供的微信模版id: TcxtCB1C9J-6ucVV5dgi4ehDva__1u8BvaB3bz-Xw1w
包含四个key: date1 thing2 number3 thing4，必须按照这个key构建消息
该template id在业务方处和account id 878026413绑定，因为限制较多，建议手动跑
"""
import json
import random
import string

import allure
import pytest

from datetime import datetime

from utils.assertions import assert_equal
from utils.http_client import TSPRequest

add_template_path = '/api/2/in/message_portal/template/add'
publish_template_path = '/api/2/in/message_portal/template/publish'
preview_template_path = '/api/2/in/message_portal/template/cn/wechat_applet/preview'
app_id = 10000


@pytest.fixture
def created_template_id(env):
    template_name = f'test_wechat_preview_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    with allure.step("创建模板"):
        template_str = {
            "template_id": "TcxtCB1C9J-6ucVV5dgi4ehDva__1u8BvaB3bz-Xw1w",
            "data": {"[#key1#]": "[#value1#]", "[#key2#]": "[#value2#]", "[#key3#]": "[#value3#]",
                     "[#key4#]": "[#value4#]"},
            "page": "",
            "properties": ""
        }
        inputs = {
            "host": env['host']['app_in'],
            "path": add_template_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": "",
            },
            "json": {
                "channel": 'wechat_applet',
                "name": template_name,
                "type": 'text',
                "template_str": json.dumps(template_str, ensure_ascii=False),
            }
        }
        response = TSPRequest.request(env, inputs)
        assert_equal(response['result_code'], 'success')
    template_id = response.get("data")
    with allure.step("发布模版"):
        inputs = {
            "host": env['host']['app_in'],
            "path": publish_template_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": {
                "id": template_id
            }
        }
        response = TSPRequest.request(env, inputs)
        assert_equal(response['result_code'], 'success')
    return template_id


@pytest.mark.skip("该template id在业务方处和account id 878026413绑定，因为限制较多，建议手动跑")
def test_wechat_applet_preview(env, created_template_id):
    with allure.step('微信小程序模板preview'):
        account_id = '878026413'
        date1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        thing2 = ''.join(random.choices(string.ascii_lowercase, k=6))
        number3 = ''.join(random.choices(string.digits, k=3))
        thing4 = ''.join(random.choices(string.ascii_uppercase, k=8))
        inputs = {
            "host": env['host']['app_in'],
            "path": preview_template_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": "",
            },
            "json": {
                "account_ids": account_id,
                "template_id": created_template_id,
                "replace_values": [{"id": account_id,
                                    "replace_map": {"key1": "date1", "value1": date1,
                                                    "key2": "thing2", "value2": thing2,
                                                    "key3": "number3", "value3": number3,
                                                    "key4": "thing4", "value4": thing4}}],
            }
        }
        response = TSPRequest.request(env, inputs)
        assert_equal(response['result_code'], 'success')
        replace_result = json.loads(response['data'][account_id])['data']
        assert_equal(replace_result['date1'], date1)
        assert_equal(replace_result['thing2'], thing2)
        assert_equal(replace_result['number3'], number3)
        assert_equal(replace_result['thing4'], thing4)
