#!/usr/bin/env python
# coding=utf-8

import json
import time

import allure
import pytest

from config.cert import web_cert
from utils.assertions import assert_equal
from utils.httptool import request


class TestSvtEventMsg(object):
    @pytest.mark.skip('manual 该case需车辆在线')
    @pytest.mark.parametrize("switch", [0, 1], ids=['switch is 0', 'switch is 1'])
    def test_svt(self, redis, env, switch):
        """
        注意，该case需车辆在线。可在盘古设置，或者手工python mqtt.py tsp-nmp-test.nioint.com ChA-0A48kgj5023-0Fc0MEB8EAEYlgkglU4oAg==

        """
        with allure.step("校验当调用接口设置svt mode时，SpecialStatus会记录svt以及svt_sample_time,重复svt set不会重复更新time"):
            vid = env['vehicles']['vehicle_for_repair']['vehicle_id']
            # vid = 'dfa6a9c86ad248c8b72974a0e7f37b2c'
            http = {
                "host": "https://tsp-test.nioint.com:4430",
                # "host": "https://tsp-stg.nioint.com:4430",
                "uri": f"/api/1/sec/in/vehicle/{vid}/svt/set_mode",
                "method": "POST",
                "params": {
                    "app_id": 10014,
                },
                "data": {
                    "switch": switch
                }
            }
            response = request(method=http['method'], url=http['host'] + http['uri'],
                               data=http['data'], params=http['params'],
                               verify=False, cert=web_cert)
            response = response.json()
            # 等待车机端返回
            time.sleep(2)
            special_status = json.loads(redis['cluster'].get(f'remote_vehicle_test:vehicle_status:{vid}:SpecialStatus'))
            assert_equal(special_status['svt'], http['data']['switch'])
            assert_equal(special_status['svt_sample_time'], response['server_time'])
