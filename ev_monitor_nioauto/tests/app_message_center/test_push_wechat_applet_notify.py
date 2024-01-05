# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_notify.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/5/13 4:36 下午
# @Description :
"""
   接口文档：http://showdoc.nevint.com/index.php?s=/647&page_id=33901
我们使用业务方提供的微信模版id: TcxtCB1C9J-6ucVV5dgi4ehDva__1u8BvaB3bz-Xw1w
包含四个key: date1 thing2 number3 thing4，必须按照这个key构建消息
该template id在业务方处和account id 878026413绑定，因为限制较多，建议手动跑
"""

import json
import allure
import pytest
from utils.http_client import TSPRequest

server_app_id = 10000
wechat_notify_path = "/api/2/in/message/wechat/applet_push"
t_id = 'TcxtCB1C9J-6ucVV5dgi4ehDva__1u8BvaB3bz-Xw1w'
send_data = {"number3": "1", "thing2": "ES6", "thing4": "北京西红门荟聚蔚来空间", "date1": "2022年05月09日 14:00"}
send_page = 'some page'
a_id = '878026413'


class TestNotify(object):
    push_im_notify_keys = "case_name,account_ids,template_id,data,page"
    push_im_notify_cases = (
        ["正案例_所有字段有值", a_id, t_id, send_data, send_page],
        ["正案例_只填必填字段", a_id, t_id, send_data, None],
        ["反案例_account_ids为None", None, t_id, send_data, send_page],
        ["反案例_template_id为None", a_id, None, send_data, send_page],
        ["反案例_data为None", a_id, t_id, None, send_page],
    )
    push_im_notify_ids = [f"{case[0]}" for case in push_im_notify_cases]

    @pytest.mark.skip("该template id在业务方处和account id 878026413绑定，因为限制较多，建议手动跑")
    @pytest.mark.parametrize(push_im_notify_keys, push_im_notify_cases, ids=push_im_notify_ids)
    def test_push_wechat_applet_notify(self, env, cmdopt, case_name, account_ids, template_id, data, page):
        app_id = 10000
        json_body = {}
        if account_ids:
            json_body['account_ids'] = account_ids
        if template_id:
            json_body['template_id'] = template_id
        if data:
            json_body['data'] = data
        if page:
            json_body['page'] = page
        inputs = {
            "host": env['host']["app_in"],
            "path": wechat_notify_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ''
            },
            "json": json_body
        }

        response = TSPRequest.request(env, inputs)
        with allure.step(""):
            if "正案例" in case_name:
                assert response['result_code'] == 'success'
            else:
                assert response['result_code'] == 'invalid_param'
