# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_template_add.py
# @Author : qiangwei.zhang
# @time: 2021/07/29
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述
import math
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.message_formator import format_to_template_list
from utils.assertions import assert_equal

server_app_id = "10000"


@pytest.mark.parametrize("case_name,res_app_id,channel,type,name,status,page_size,page_num", [
    ("正案例_根据channel查询_email", "10000", "email", None, None, None, None, None),
    ("正案例_根据channel查询_email", "100480", "email", None, None, None, None, None),
    ("正案例_根据channel查询_sms", "10000", "sms", None, None, None, None, None),
    ("正案例_根据channel查询_不存在", "10000", "not_exist", None, None, None, None, None),
    ("正案例_根据type查询_text", "10000", "email", "text", None, None, None, None),
    ("正案例_根据type查询_h5", "10000", "email", "h5", None, None, None, None),
    ("正案例_根据type查询_not_exist", "10000", "email", "not_exist", None, None, None, None),
    ("正案例_根据name查询", "10000", "email", None, "email", None, None, None),
    ("正案例_根据status查询", "10000", "email", None, None, 1, None, None),
    ("正案例_各条件组合查询", "10000", "email", "h5", 'email', 1, 5, 1),
    ("正案例_自定义page_size", "10000", "email", None, None, None, 20, None),
    ("正案例_自定义page_num", "10000", "email", None, None, None, 20, 2),
    ("正案例_自定义page_num", "10000", "email", None, None, None, 5, 5),
])
def test_template_list(env, mysql, cmdopt, case_name, res_app_id, channel, type, name, status, page_size, page_num):
    """
    """
    retry_num = 20
    with allure.step('查询消息模版列表接口'):
        path = "/api/2/in/message_portal/template/list"
        params = {"region": "cn", "lang": "zh-cn", "hash_type": "sha256",
                  "app_id": res_app_id, "channel": channel, "name": name, "type": type,
                  "status": status, "page_size": page_size, "page_num": page_num,
                  "sign": "yes"
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
            where_model = {"valid": 1}
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
                    where_model['template_id'] = value
                    break
            template_list = mysql["nmp_app"].fetch("message_template", where_model=where_model, order_by="id",
                                                   suffix=f"limit {(page_num - 1) * page_size},{page_size}",
                                                   retry_num=retry_num)
            total_template = mysql["nmp_app"].fetch("message_template", where_model=where_model, fields=["count(1) as total_num"], retry_num=retry_num)

            page = format_to_template_list(template_list, cmdopt)
            except_result = {
                "data": {
                    "page": page,
                    "pagination": {
                        "totalNum": total_template[0].get("total_num"),
                        "totalPageNum": math.ceil(total_template[0].get("total_num") / page_size),
                        "pageNum": page_num,
                        "pageSize": page_size
                    }
                },
                "result_code": "success",
            }
            assert_equal(response, except_result)
        else:
            if not channel:
                response.pop("request_id")
                response.pop("server_time")
                expected_res = {
                    "result_code": "internal_error",
                    "debug_msg": "Required String parameter 'channel' is not present"
                }
                assert_equal(expected_res, response)
            if server_app_id != res_app_id:
                response.pop("request_id")
                response.pop("server_time")
                expected_res = {
                    "result_code": "invalid_param",
                    "debug_msg": "invalid template id"
                }
                assert_equal(expected_res, response)
