# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : vehicle_online.py
# @Author : qiangwei.zhang
# @time: 2022/04/19
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述 车辆在线接口

from utils.http_client import TSPRequest as hreq


def vehicle_online(env, vid, ecu):
    cmdopt = env["cmdopt"]
    env_str_map = {"test_marcopolo": "intl-test", "stg_marcopolo": "stg-eu"}
    env_str = env_str_map.get(cmdopt, cmdopt)
    inputs = {
        "host": "http://pangu.nioint.com:5000",
        "path": "/vcontrol/mqtt_connect",
        "method": "POST",
        "params": {"vid": vid, "ecu": ecu, "env": env_str},
    }
    response = hreq.request(env, inputs)
    if response.get("result_code") == "success":
        return True
    else:
        return False
