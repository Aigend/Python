#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    app_bind  http://showdoc.nevint.com/index.php?s=/13&page_id=624
    app_update   http://showdoc.nevint.com/index.php?s=/13&page_id=627
    app_unbind  http://showdoc.nevint.com/index.php?s=/13&page_id=630

    * 在类似于HU系统中，有一个公共的Notification Center，在Notification Center 中获取消息之后会将此消息根据package name 发送到对应的app。为了支持此功能，消息平台支持App绑定与解绑的功能。
        例如：
        APP发送导航到车机，调用notify_hu接口。其中target_app_ids = '30010'。而该app做了绑定
           app_id	base_app_id	pkg_name	    update_time
           30010	30007	    com.nio.nomi	2017-10-30 06:17:49
        所以消息先下发到CDC的Notification Center（30007），然后Center再根据具体的target_app_ids下发消息到最终的接收端（30010）

"""
import allure
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq

app_bind_path = "/api/1/in/message/app_bind"
app_update_path = "/api/1/in/message/app_update"
app_unbind_path = "/api/1/in/message/app_unbind"


def test_app_bind_update_unbind(env, mysql):
    app_id = "10001"
    host = env['host']['app_in']
    app_bind_inputs = {
        "host": host,
        "path": app_bind_path,
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "params": {"app_id": app_id, "sign": ""},
        "data": {'nonce': 'MrVIRwkCLBKySgCG', 'base_app_id': app_id, 'pkg_name': '123123'}
    }
    with allure.step('app bind'):
        response = hreq.request(env, app_bind_inputs)
        assert response.get("result_code") == "success"
    with allure.step('app update'):
        update_inputs = {
            "host": host,
            "path": app_update_path,
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {"app_id": app_id, "sign": ""},
            "data": {'nonce': 'MrVIRwkCLBKySgCG', 'base_app_id': app_id, 'pkg_name': '123123'}
        }
        response = hreq.request(env, update_inputs)
        assert response.get("result_code") == "success"
        with allure.step("校验mysql"):
            pkg_name = mysql['nmp_app'].fetch('app_bindings', {'app_id': app_id}, ['pkg_name'])[0]['pkg_name']
            assert_equal(pkg_name, '123123')
        app_unbind_inputs = {
            "host": host,
            "path": app_unbind_path,
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {"app_id": app_id, "sign": ""},
            "data": {'nonce': 'MrVIRwkCLBKySgCG', 'base_app_id': app_id, 'pkg_name': '123123'}
        }
        with allure.step('app_unbind'):
            response = hreq.request(env, app_unbind_inputs)
            assert response.get("result_code") == "success"
