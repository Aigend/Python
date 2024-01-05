#!/usr/bin/env python
# coding=utf-8

"""
@author: chunming.liu
@Date: 2019/1/17
@Feature: 1)如果车辆离线，发送实时消息前，evm_server主动给国家和地方平台发送一个车辆login消息。
"""
import random

import allure

from nio_messages import wti
import json
import pytest
import time
from utils.commonlib import show_json
from utils.time_parse import time_sec_to_strtime


class TestLoginBeforeChargeUpdateAutomatically(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, env, kafka, publish_msg_by_kafka):
        host = env['host']['tsp_in']
        attribution = env['vehicles']['sh_private']['attribution']

        vin = env['vehicles']['sh_private']['vin']
        vid = env['vehicles']['sh_private']['vehicle_id']
        nextev_message, obj = publish_msg_by_kafka('charge_end_event', vin=vin, vid=vid)

        return host, attribution

    @pytest.mark.skip('manual')
    def test_login_before_charge_update(self, env, mysql, prepare, publish_msg_by_kafka):
        # 上报
        vin = env['vehicles']['sh_private']['vin']
        vid = env['vehicles']['sh_private']['vehicle_id']

        alarm_singal_list = random.sample(wti.EVM_WTI_SIGNAL, 4)
        nextev_message, obj = publish_msg_by_kafka('periodical_charge_update',
                                                   vin=vin, vid=vid,
                                                   sample_points=[{
                                                       'alarm_signal':
                                                           {'signal_int': alarm_singal_list}}])
        time.sleep(10)
        # 校验
        # sh_message_mock_server = mysql['rvs'].fetch('vehicle_data_mock',
        #                                             {"vin": vin,
        #                                              "sample_time": obj['sample_points'][0]['sample_ts']//1000,
        #                                              "attribution": prepare[1],
        #                                              "command": "1"  # 表示车辆登入消息
        #                                              }
        #                                             )[0]
        sample_time = time_sec_to_strtime(obj['sample_points'][0]['sample_ts'] // 1000)
        gb_message_mock_server = mysql['rvs'].fetch('vehicle_data_mock',
                                                    {"vin": vin,
                                                     "sample_time>=": sample_time,
                                                     "attribution": '156',
                                                     "command": "1"  # 表示车辆登入消息
                                                     }
                                                    )[0]

        # with allure.step("校验BJ Mock Server收到了转发login"):
        #     allure.attach( show_json(sh_message_mock_server),"mock_server收到的内容")
        #     sh_message_mock_server = json.loads(sh_message_mock_server['message'])
        #     assert sh_message_mock_server['unique_id'] == env['vehicles']['sh_private']['vin']
        #     assert sh_message_mock_server['data_unit'] is not None

        with allure.step("校验GB Mock Server收到了转发login"):
            allure.attach(show_json(gb_message_mock_server), "mock_server收到的内容")
            gb_message_mock_server = json.loads(gb_message_mock_server['message'])
            assert gb_message_mock_server['uniqueId'] == env['vehicles']['sh_private']['vin']
            assert gb_message_mock_server['dataUnit'] is not None
