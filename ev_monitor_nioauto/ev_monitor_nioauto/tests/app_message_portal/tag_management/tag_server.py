# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : tag_server.py
# @Author : qiangwei.zhang
# @time: 2021/12/23
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import pytest
import time
import json
from utils.http_client import TSPRequest as hreq
from utils.logger import logger

tag_add_path = "/api/2/in/message_portal/tag/add"
tag_publish_path = "/api/2/in/message_portal/tag/publish"
account_type_map = {"account_id": 1, "user_id": 2, "mobile_num": 3, "email": 4}


def add_tag(env, account_type="account_id", name="server_add", url="http://serveradd.url", app_id=10000):
    with allure.step('创建新的tag'):
        inputs = {
            "host": env['host']['app_in'],
            "path": tag_add_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "type": account_type_map.get(account_type),
                "name": name,
                "url": url,
            }
        }
        response = hreq.request(env, inputs)
        assert response.get("result_code") == "success"
        return response.get("data")


def get_published_tag(env, mysql, account_type="account_id", name="server_add", url="http://serveradd.url", app_id=10000):
    with allure.step(""):
        mysql_results = mysql['nmp_app'].fetch("remote_tag", {"status": 9, "app_id": app_id})
        if mysql_results:
            return mysql_results[0].get("id")
    with allure.step('创建新的tag'):
        inputs = {
            "host": env['host']['app_in'],
            "path": tag_add_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "type": account_type_map.get(account_type),
                "name": name,
                "url": url,
            }
        }
        response = hreq.request(env, inputs)
        assert response.get("result_code") == "success"
        tag_id = response.get("data")
    with allure.step("发布tag"):
        inputs = {
            "host": env['host']['app_in'],
            "path": tag_publish_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "id": tag_id
            }
        }
        response = hreq.request(env, inputs)
        assert response.get("result_code") == "success"
        return tag_id


def add_tag_and_publish(env, mysql, account_type="account_id", name="server_add", url="http://serveradd.url", app_id=10000):
    tags = mysql["nmp_app"].fetch("remote_tag", {"status": 9, "name": name, "type": account_type_map.get(account_type), "url": url}, suffix="order by update_time desc",
                                  retry_num=2)
    if tags:
        return tags[0].get("id")
    with allure.step('创建新的tag'):
        inputs = {
            "host": env['host']['app_in'],
            "path": tag_add_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "type": account_type_map.get(account_type),
                "name": name,
                "url": url,
            }
        }
        response = hreq.request(env, inputs)
        assert response.get("result_code") == "success"
        tag_id = response.get("data")
    with allure.step("发布tag"):
        inputs = {
            "host": env['host']['app_in'],
            "path": tag_publish_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "id": tag_id
            }
        }
        response = hreq.request(env, inputs)
        assert response.get("result_code") == "success"
        return tag_id


def init_tag(env, mysql):
    cmdopt = env["cmdopt"]
    init_tag_list = [
        ("all", "email", "init_email", "http://pangu.nioint.com:5000/pangu/get_tag_email", 10000),
        ("all", "account_id", "init_fake_id", "http://pangu.nioint.com:5000/pangu/get_tag_fake_id_page_2k", 10000),
        ("all", "account_id", "init_fake_url", "http://pangu.nioint.com:5000/pangu/get_fake_url", 10000),
        ("all", "mobile_num", "init_mobile_num", "http://pangu.nioint.com:5000/pangu/get_tag_mobile_num", 10000),
        ("test", "user_id", "init_user_id", "http://pangu.nioint.com:5000/pangu/get_tag_test_user_id", 10000),
        ("test", "account_id", "init_account_id", "http://pangu.nioint.com:5000/pangu/get_tag_test_account_id", 10000),
        ("test_marcopolo", "account_id", "init_account_id", "http://pangu.nioint.com:5000/pangu/get_tag_test_account_id", 10000),
        ("test_marcopolo", "user_id", "init_user_id", "http://pangu.nioint.com:5000/pangu/get_tag_test_user_id", 10000),
        ("stg_marcopolo", "user_id", "init_user_id", "http://pangu.nioint.com:5000/pangu/get_tag_stg_user_id", 10000),
        ("stg_marcopolo", "account_id", "init_account_id", "http://pangu.nioint.com:5000/pangu/get_tag_stg_account_id", 10000),
    ]
    tag_map = {}
    for tag in init_tag_list:
        env_str, account_type, name, url, app_id = tag
        if env_str == "all" or cmdopt == env_str:
            tag_map[name] = add_tag_and_publish(env, mysql, account_type, name, url, app_id=10000)
    return tag_map
