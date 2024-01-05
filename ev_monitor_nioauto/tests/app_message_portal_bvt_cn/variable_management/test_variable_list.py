# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_variable_list.py
# @Author : qiangwei.zhang
# @time: 2021/08/03
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import math
import allure
import pytest
from utils.random_tool import random_string
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_portal.variable_management.variable_server import create_new_variable, delete_variable
from utils.message_formator import format_to_variable_list
from utils.assertions import assert_equal


@pytest.mark.parametrize("case_name,app_id,url,name,status,id,page_size,page_num", [
    ("正案例_根据url", "10000", "http", None, None, None, None, None),
    ("正案例_根据url", "100480", "http", None, None, None, None, None),
    ("正案例_根据name", "10000", None, "新增参数", None, None, None, None),
    ("正案例_根据status", "10000", None, None, 1, None, None, None),
    ("正案例_根据id", "10000", None, None, None, 'id', None, None),
    ("正案例_指定page_size", "10000", None, None, 1, None, 5, None),
    ("正案例_指定page_num", "10000", None, None, 1, None, None, 2),
    ("正案例_指定page_size+page_num", "10000", None, None, 1, None, 4, 2),
    ("正案例_指定page_size+page_num", "10000", None, None, None, None, None, None),
    ("正案例_指定page_size+page_num", "10000", None, "not_exist", None, None, None, None),
])
def test_variable_list(env, cmdopt, mysql, case_name, app_id, url, name, status, id, page_size, page_num):
    """
    """
    retry_num = 20
    if id:
        variable = create_new_variable(env, mysql)
        id = variable.get("id")
    with allure.step('查询远程参数列表接口'):
        path = "/api/2/in/message_portal/variable/list"
        params = {"region": "cn", "lang": "zh-cn", "hash_type": "sha256",
                  "app_id": app_id, "name": name, "status": status, "id": id,
                  "page_size": page_size, "page_num": page_num, "sign": "yes"
                  }
        params = {k: v for k, v in params.items() if v}
        page_size = page_size if page_size else 10
        page_num = page_num if page_num else 1
        inputs = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "GET",
            "params": params
        }
        response = hreq.request(env, inputs)
        logger.debug(response)
        with allure.step('查询远程参数列表接口校验'):
            response.pop("request_id")
            response.pop("server_time")
            where_model = {}
            for key, value in params.items():
                if value == "not_exist":
                    retry_num = 1
                if key in ['status', "app_id"]:
                    where_model[key] = value
                if key in ['name', "url"]:
                    where_model[f"{key} like"] = f"%{value}%"
                if key == "id":
                    # 如果传了ID其他条件无效
                    where_model.clear()
                    where_model['id'] = value
                    break
            variable_list = mysql["nmp_app"].fetch("remote_variable", where_model=where_model, order_by="id",
                                                   suffix=f"limit {(page_num - 1) * page_size},{page_size}",
                                                   retry_num=retry_num)
            total_variable = mysql["nmp_app"].fetch("remote_variable", where_model=where_model, fields=["count(1) as total_num"], retry_num=retry_num)

            page = format_to_variable_list(variable_list, cmdopt)
            except_result = {
                "data": {
                    "page": page,
                    "pagination": {
                        "totalNum": total_variable[0].get("total_num"),
                        "totalPageNum": math.ceil(total_variable[0].get("total_num") / page_size),
                        "pageNum": page_num,
                        "pageSize": page_size
                    }
                },
                "result_code": "success",
            }
            assert_equal(except_result, response)
            if id:
                delete_variable(env, mysql, id)
