# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : variable_server.py
# @Author : qiangwei.zhang
# @time: 2021/08/02
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :远程变量相关api

import allure
import os
from utils.random_tool import random_string, format_time
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
import re
from config.settings import BASE_DIR

public_variable_format = r'(\[\*.*?\*\])'
public_variable_format_name = r'\[\*(.*?)\*\]'
private_variable_format = r'(\[\#.*?\#\])'
private_variable_format_name = r'\[\#(.*?)\#\]'

variable_name_url_map = {
    "qa_user_name": "http://pangu.nioint.com:5000/pangu/get_user_name",
    "qa_city": "http://pangu.nioint.com:5000/pangu/get_city",
    "qa_part_user": "http://pangu.nioint.com:5000/pangu/get_part_variable",
    "qa_random_str": "http://pangu.nioint.com:5000/pangu/get_variable",
}

add_variable_path = "/api/2/in/message_portal/variable/add"
publish_variable_path = "/api/2/in/message_portal/variable/publish"
delete_variable_path = "/api/2/in/message_portal/variable/delete"
detail_variable_path = "/api/2/in/message_portal/variable/detail"
app_id = 10000


def create_new_variable(env, mysql, channel="email", content_type='text'):
    with allure.step('添加参数接口'):
        name = f"QA_{channel}_{content_type}_{random_string(13)}"
        http = {
            "host": env['host']['app_in'],
            "path": add_variable_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "name": name,
                "url": f"http://pangu.nioint.com:5000/pangu/get_variable",
            }
        }
        response = hreq.request(env, http)
        assert response['result_code'] == 'success'
        variable = mysql["nmp_app"].fetch("remote_variable", {"name": name})
        variable_id = variable[0].get("id")
        logger.debug(f'variable_id:{variable_id}')
        return variable[0]


def get_published_variable_id(env, mysql, t_app_id=10000):
    variable = mysql["nmp_app"].fetch("remote_variable", {"status": 9, "app_id": t_app_id}, retry_num=5)
    if variable:
        return variable[0].get("id")
    else:
        new_variable = create_new_variable(env, mysql)
        new_variable_id = new_variable.get("id")
        with allure.step('发布公共参数接口'):
            http = {
                "host": env['host']['app_in'],
                "path": publish_variable_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": t_app_id, "sign": ""},
                "json": {"id": new_variable_id}
            }
            response = hreq.request(env, http)
            assert response['result_code'] == 'success'
            with allure.step('校验mysql模板状态为9已发布'):
                variable = mysql["nmp_app"].fetch("remote_variable", {"status": 9})
                assert len(variable) == 1
                return new_variable_id


def delete_variable(env, mysql, variable_id):
    variable = mysql["nmp_app"].fetch("remote_variable", {"id": variable_id})
    if variable and variable[0].get("status") != 9:
        with allure.step('删除公共变量接口'):
            http = {
                "host": env['host']['app_in'],
                "path": delete_variable_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": {"id": variable_id}
            }
            response = hreq.request(env, http)
            assert response['result_code'] == "success"
            with allure.step('校验mysql模板被删除'):
                variable = mysql["nmp_app"].fetch("remote_variable", {"id": variable_id}, retry_num=1)
                assert len(variable) == 0
                return "success"
    else:
        return "公共变量不存在或已发布不可被删除"


def get_variable_detail(env, variable_id):
    with allure.step('根据id获取公共变量详情接口'):
        http = {
            "host": env['host']['app_in'],
            "path": detail_variable_path,
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn",
                       "lang": "zh-cn",
                       "hash_type": "sha256",
                       "app_id": app_id,
                       'id': variable_id
                       }
        }
        response = hreq.request(env, http)
        logger.debug(response)
        assert response['result_code'] == 'success'
        return response


def published_variable(env, mysql, variable_id):
    variable = mysql["nmp_app"].fetch("remote_variable", {"status": 9, "id": variable_id}, retry_num=5)
    if variable:
        return f"参数{variable_id}，已是发布状态无需再发布"
    else:
        with allure.step('发布远程参数接口'):
            http = {
                "host": env['host']['app_in'],
                "path": publish_variable_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": {"id": variable_id}
            }
            response = hreq.request(env, http)
            assert response['result_code'] == 'success'
            with allure.step('校验mysql模板状态为9已发布'):
                variable = mysql["nmp_app"].fetch("remote_variable", {"status": 9, "id": variable_id})
                assert len(variable) == 1
            return f"公共参数{variable_id}已发布"


def create_variable_and_published(env, mysql, name, url):
    cmdopt = env['cmdopt']
    variable = mysql["nmp_app"].fetch("remote_variable", {"name": name}, retry_num=2)
    if variable:
        if 'stg' not in cmdopt:
            mysql["nmp_app"].update("remote_variable", {"name": name}, {"url": url})
        variable_id = variable[0].get("id")
        return variable_id
    else:
        with allure.step('添加参数接口'):
            http = {
                "host": env['host']['app_in'],
                "path": add_variable_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": {
                    "name": name,
                    "url": url,
                }
            }
            response = hreq.request(env, http)
            assert response['result_code'] == 'success'
            variable = mysql["nmp_app"].fetch("remote_variable", {"name": name})
            variable_id = variable[0].get("id")
            logger.debug(f'variable_id:{variable_id}')
        return variable_id


def init_variable(env, mysql):
    variable_name_id_map = {}
    for name, url in variable_name_url_map.items():
        variable_id = create_variable_and_published(env, mysql, name, url)
        variable_name_id_map[name] = variable_id
        published_variable(env, mysql, variable_id)
    return variable_name_id_map


def generate_private_variable_replace(user_ids, variables, part_user=False, part_variable=False):
    replace_values = []
    user_index = 0
    if user_ids:
        for user_id in user_ids.split(','):
            user_info, replace_map = {}, {}
            if part_user:
                if user_index % 2:
                    continue
            user_info["id"] = user_id
            user_info["replace_map"] = replace_map
            variable_index = 0
            if variables:
                for variable in variables.split(','):
                    if part_variable:
                        if variable_index % 2:
                            continue
                    replace_map[variable] = f"QA_RS_{random_string(10)}"
                    variable_index += 1
                user_info["replace_map"] = replace_map
                user_index += 1
            replace_values.append(user_info)
    return replace_values


def generate_global_private_variable_replace(variables):
    replace_values = []
    user_info, replace_map = {}, {}
    user_info["id"] = "GLOBAL"
    user_info["replace_map"] = replace_map
    if variables:
        for variable in variables.split(','):
            replace_map[variable] = f"QA_RS_{random_string(10)}"
        user_info["replace_map"] = replace_map
    replace_values.append(user_info)
    return replace_values


def extracted_variable_from_template(template_str):
    public_variable = list(set(re.findall(public_variable_format, template_str)))
    private_variable = list(set(re.findall(private_variable_format_name, template_str)))
    return public_variable, private_variable


def extracted_private_variable_from_template(template_str):
    private_variable_name = list(set(re.findall(private_variable_format_name, template_str)))
    private_variable_str = ','.join(private_variable_name)
    return private_variable_str


def verify_variable(response, user_info, replace_values=None):
    user_replace_map = {}
    assert response.get("result_code") == "success"
    data = response.get("data")
    assert len(data) == len(user_info.split(",")) + 1
    template_str = data.pop("default")
    public_variables, private_variables = extracted_variable_from_template(template_str)
    if replace_values:
        user_replace_map = {user_replace.get("id"): user_replace.get("replace_map") for user_replace in replace_values}
    for user in user_info.split(","):
        user_content = data.get(str(user))
        if not public_variables and not private_variables:
            assert template_str == user_content
        if public_variables:
            for public_variable in public_variables:
                assert f"[*{public_variable}*]" not in user_content
        if private_variables:
            for private_variable in private_variables:
                if user_replace_map.get(user):
                    if user_replace_map.get(user).get(private_variable):
                        assert user_replace_map.get(user).get(private_variable) in user_content
                else:
                    assert f"[#{private_variable}#]" in user_content, f"Except [#{private_variable}#] Actual {user_content}"


if __name__ == '__main__':
    # template_str = "[#name#][*name*][#name#][#age#]"
    # public_variable, private_variable = extracted_variable_from_template(template_str)
    # private_variable_str = extracted_private_variable_from_template(template_str)
    # logger.debug(public_variable)
    # logger.debug(private_variable)
    # logger.debug(private_variable_str)

    file_path = f'./account_ids.txt'
    account_list = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            user_id_list = [u.replace('\n', '') for u in lines]
            user_ids = ",".join(user_id_list)

    variables = "user_name,model_name,time,service_center_name,phone_number,email_address"
    res = generate_private_variable_replace(user_ids, variables, )
    logger.debug(res)
    res = [{'id': '550736273@qq.com', 'replace_map': {'city': '北京', 'activity': '清凉一夏', 'date': '2021年9月1日'}},
           {'id': '842244250@qq.com', 'replace_map': {'city': '郑州', 'activity': '试驾活动', 'date': '2021年9月6日'}}]
