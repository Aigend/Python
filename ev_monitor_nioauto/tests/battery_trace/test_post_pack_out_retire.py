# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2022/01/17
@api: POST_/api/1/in/battery/pack_out_retire
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=32319
@description: 本质上是为了退役而做的接口，只是国家平台要求先出库再退役，才合并到一起的。并且不是实时退役，而是先存于tsp，给PE部门的调用方返回成功，然后每日定时任务尝试上报到国家平台。(task 11)
"""
import allure
import pytest

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as restClient

app_id = 100078


@pytest.fixture(autouse=True, scope='module')
def get_code(env):
    with allure.step('使用graphql查询电池模组列表'):
        graphql = f"""
        {{
            packs (page: 1, page_size: 1, start_time:"", code: "", nio_encoding: "", status: -2, model_id: "", export: false) {{
                page
                page_size
                total
                export_id
                list {{
                    code
                    nio_encoding
                    status
                    source
                    manufacturing_date
                    logistic_des
                }}
            }}
        }}
        """
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/graphql',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": {'query': graphql}
        }
        response = restClient.request(env, http)
        return response['data']['packs']['list'][0]['code']


@pytest.mark.parametrize('code, out_time, unit_code, unit_name, remark, expectation, check_db',
                         [(True, '2020-01-01 00:00:00', '91330800575349959F', '衢州华友钴新材料有限公司', None, 'success', True),
                          (False, '2020-01-01 00:00:00', '91330800575349959F', '衢州华友钴新材料有限公司', 'test', 'invalid_param', False),
                          (True, None, '91330800575349959F', '衢州华友钴新材料有限公司', 'test', 'invalid_param', False),
                          (True, '2020-01-01 00:00:00', None, '衢州华友钴新材料有限公司', 'test', 'invalid_param', False),
                          (True, '2020-01-01 00:00:00', '91330800575349959F', None, 'test', 'invalid_param', False)],
                         ids=['已填写所有必要参数', '参数未包含电池包编码', '参数未包含出库日期', '参数未包含去向单位统一社会信用代码', '参数未包含出库电池包去向单位名称'])
def test_post_pack_out_retire(env, get_code, mysql, code, out_time, unit_code, unit_name, remark, expectation, check_db):
    with allure.step('电池出库并且退役'):
        json = {'out_time': out_time, 'destination_unit_code': unit_code, 'destination_unit_name': unit_name, 'remark': remark}
        json = {k: v for k, v in json.items() if v is not None}
        if code:
            json['code'] = get_code
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/pack_out_retire',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": json
        }
        response = restClient.request(env, http)
        with allure.step('校验response'):
            assert_equal(response['result_code'], expectation)
            if check_db:
                record = mysql['battery_trace'].fetch_one('retire', {'code': get_code})
                assert record
