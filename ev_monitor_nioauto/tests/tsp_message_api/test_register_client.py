#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/13 12:01
@contact: li.liu2@nio.com
@description:
    注册client_id
    http://showdoc.nevint.com/index.php?s=/13&page_id=1070

    * 该接口用于注册车，app，充电桩的mqtt client
    * 此API用于客户端从NMP获取一个独一无二的ClientID。客户端需要使用这个ClientID，以及User/Password（根据业务需求）连接到MessageServer。因此客户端需要在本地存储此ClientID。
    * 根据不同设备特性，有些客户端使用相同的请求每次获取的ClientID都不相同，例如用户手机。而另一些客户端的ClientID每次获取的一样，比如车机HU／Fellow App等。原因是生成的ClientID是否信任DeviceID是全局唯一的，如果不是全局唯一的，那么就应该选择第一个方式生成ClientID
    * 根据不同设备特性，ClientID是有可能过期的，因此在启动连接的时候需要通过Update Client接口，确定ClientID是否有效，同时Update Client也是报活的一个方式。
    * 为了避免恶意访问，目前我们设置了该接口的访问频次。
    * register client logic: https://confluence.nioint.com/display/CVS/NMP+Client+Logic
    * Message API: https://confluence.nioint.com/display/CVS/Message+API
    * 唯一client_id 白名单。在该白名单下的appid，重新登录时只要device_id不变就不会更换client_id信息
        app_unique_client_white_list:10002,10018,30007,10003
        tsp_unique_client_white_list:10005,10107

"""

import time
import allure
import pytest
from config.settings import tsp_vehicle_auth
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


class TestMessageAPI(object):
    register_client_keys = "case_name,app_id,platform,ecu,host_name,vehicle_key,hash_type"
    register_client_cases = [
        # NT1 车辆
        ["NT1_CGW注册client", 10005, "NT1", 'cgw', "tsp_ex", "v1", "sha256"],
        # ["NT1_ADC注册client", 10107, "NT1", 'adc', "tsp_ex", "v2", "sha256"],
        # ["NT1_CGW注册client", 10005, "NT1", 'cgw', "v_in_4430", "v1", "md5"],
        # ["NT1_ADC注册client", 10107, "NT1", 'adc', "v_in_4430", "v2", "sha256"],
        # NT2 车辆
        # ["NT2_SA注册client", 10005, "NT2", 'sa', "v_in_4430", "v1", "sha256"],
        # ["NT2_ADC注册client", 100512, "NT2", 'adc', "adc_ex_4430", "v2", "sha256"],
    ]
    register_client_ids = [f"{case[0]}" for case in register_client_cases]

    @pytest.mark.parametrize(register_client_keys, register_client_cases, ids=register_client_ids)
    def test_register_client(self, env, cmdopt, mysql, case_name, app_id, platform, ecu, host_name, vehicle_key, hash_type):
        # 用不同的车绕过频率控制
        with allure.step(f"register_client接口{case_name}"):
            # vehicle_key = 'v2' if platform == "NT1" and app_id == 10107 else "v1"
            vehicle_id = env['vehicles']['register_client'][platform][vehicle_key]["vid"]
            vehicle_cert = tsp_vehicle_auth(cmdopt, vehicle_id, platform)
            inputs = {
                "host": env['host'][host_name],
                "path": "/api/1/message/register_client",
                "method": "POST",
                "headers": {'Content-Type': 'application/x-www-form-urlencoded'},
                'params': {
                    'app_id': app_id,
                    'region': 'cn',
                    'lang': 'zh_cn',
                    "hash_type": hash_type,
                    'sign': '',
                },
                'data': {
                    'app_version': '1.3.4',
                    'brand': 'xiaomi',
                    'device_type': 'vehicle',
                    'device_token': '',
                    'device_id': vehicle_id,
                    'os': 'android',
                    'os_version': '6.0',
                    'nonce': str(int(time.time() * 1000))
                },
                "verify": False,
                "cert": vehicle_cert.get(f"{ecu}_cert"),
            }
            response = hreq.request(env, inputs)
        with allure.step("校验结果"):
            assert response['result_code'] == "success"
            db_res = mysql['nmp'].fetch("clients", {"device_id": vehicle_id, "app_id": app_id})
            client_id = db_res[0].get("client_id")
            expect_res = {"data": {"client_id": client_id}, "result_code": "success", }
            response.pop("request_id")
            response.pop("server_time")
            assert_equal(response, expect_res)
