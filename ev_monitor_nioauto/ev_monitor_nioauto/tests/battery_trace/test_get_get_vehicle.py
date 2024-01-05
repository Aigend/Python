# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author:colin.li
@time: 2021/08/04
@api: GET_/api/1/in/battery/get_vehicle
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=27859
@description: 通过vin或vid查询电池包编码
"""

import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal

app_id = 100078
get_vehicle_path = '/api/1/in/battery/get_vehicle'


def test_get_get_vehicle(env, mysql):
    sql = "select sv.`code` as code, sv.vin as vin, sv.vehicle_id as vehicle_id, sbpe.nio_encoding as nio_encoding, sbpe.bid as bid  from sys_veh sv , sys_battery_pack_entity sbpe where sv.code = sbpe.code limit 1"
    mysql_res = mysql['battery_trace'].fetch_by_sql(sql)
    if not mysql_res:
        assert "错误信息" == "数据库无数据"
    expect_data = mysql_res[0]
    expect_res = {
        "result_code": "success",
        "data": expect_data
    }
    vin = expect_data.get("vin")
    with allure.step(f'查询vin为{vin}的车对应的电池编码'):
        http = {
            "host": env['host']['tsp_in'],
            "path": get_vehicle_path,
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
                "vin": vin
            },
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        response.pop("request_id")
        response.pop("server_time")
        response.pop("debug_msg")
        assert_equal(response, expect_res)
