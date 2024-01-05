# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_task_list.py
# @Author : qiangwei.zhang
# @time: 2021/08/09
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import pytest
import math
import json
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_portal.task_management.task_server import create_task
from utils.message_formator import format_to_task_list
from utils.assertions import assert_equal

task_list_path = "/api/2/in/message_portal/task/list"


@pytest.mark.parametrize("case_name,app_id,status,id,page_size,page_num", [
    ("正案例_根据查询所有", "10000", None, None, None, None),
    ("正案例_根据查询所有", "10000", 1, None, None, None),
    ("正案例_根据查询所有", "10000", None, "1", None, None),
])
def test_task_list(env, mysql, cmdopt, case_name, app_id, status, id, page_size, page_num):
    retry_num = 20
    task_id = None
    if id:
        task_id = create_task(env, mysql)
    with allure.step('查询消息模版列表接口'):
        path = "/api/2/in/message_portal/task/list"
        params = {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "status": status,
                  "id": task_id, "page_size": page_size, "page_num": page_num, "sign": "yes"
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
        if case_name.startswith("正案例"):
            response.pop("request_id")
            response.pop("server_time")
            where_model = {}
            for key, value in params.items():
                if value == "not_exist":
                    retry_num = 1
                if key in ['channel', 'type', 'status', "app_id"]:
                    where_model[key] = value
                if key == "name":
                    where_model[f"{key} like"] = f"%{value}%"
                if key == "id":
                    # 如果传了ID其他条件无效
                    where_model.clear()
                    where_model['id'] = value
                    break
            task_list = mysql["nmp_app"].fetch("message_task", where_model=where_model, order_by="id",
                                               suffix=f"limit {(page_num - 1) * page_size},{page_size}",
                                               retry_num=retry_num)
            total_task = mysql["nmp_app"].fetch("message_task", where_model=where_model, fields=["count(1) as total_num"], retry_num=retry_num)

            page = format_to_task_list(task_list, cmdopt)
            except_result = {
                "data": {
                    "page": page,
                    "pagination": {
                        "totalNum": total_task[0].get("total_num"),
                        "totalPageNum": math.ceil(total_task[0].get("total_num") / page_size),
                        "pageNum": page_num,
                        "pageSize": page_size
                    }
                },
                "result_code": "success",
            }
            assert_equal(except_result, response)
            # if id:
            #     delete_task(env, mysql, id)
