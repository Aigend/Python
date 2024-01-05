#!/usr/bin/env python
# coding=utf-8

"""
:file: test_instant_status_resp_cassandra.py
:author: muhan.chen
:Date: Created on 2018/5/30 下午5:18
:Description: 上报车辆的全量数据
"""
import time

import pytest
import allure

list_situation = (False, True)
case = []
for i in list_situation:
    if i is True:
        srr = 'set_outside_sample_ts=' + str(i) + ', use outside sample_ts.'
        case.append(srr)
    if i is False:
        srr = 'set_outside_sample_ts=' + str(i) + ', use inside sample_ts.'
        case.append(srr)


@allure.feature('上报车辆的全量事件')
class TestInstantStatusMsg(object):
    @allure.story('车机处于离线状态，当恢复在线状态上报此事件，保证app显示为最新的车辆状态')
    @pytest.mark.parametrize("set_outside_sample_ts", list_situation, ids=case)
    def test_instant_status_resp(self, publish_msg, checker, set_outside_sample_ts):
        # 构造并上报消息
        if set_outside_sample_ts:
            nextev_message, instant_status_obj = publish_msg('instant_status_resp', protobuf_v=18, platform_type=1,
                                                             signallib_version='BL00.07.00_DA_01',
                                                             outside_sample_ts=int(round(time.time() * 1000)),
                                                             )
        else:
            nextev_message, instant_status_obj = publish_msg('instant_status_resp')
        # 校验
        if 'sample_ts' in instant_status_obj:
            cassandra_time = instant_status_obj['sample_ts']
        else:
            cassandra_time = instant_status_obj['sample_point']['sample_ts']

        tables = {'vehicle_data': ['vehicle_id',
                                   'charging_info',
                                   'soc_status',
                                   'trip_status',
                                   'body_status',
                                   'position_status',
                                   'vehicle_status',
                                   'bms_status',
                                   'driving_data',
                                   'driving_motor_status',
                                   'extremum_data',
                                   'occupant_status',
                                   'hvac_status',
                                   'tyre_status',
                                   'can_msg',
                                   'can_signal',
                                   'window_status',
                                   'light_status',
                                   'door_status',
                                   'btry_pak_info',
                                   # 're_alarm_data',
                                   'alarm_data',
                                   'evm_flag',
                                   'sample_ts']
                  }
        checker.check_cassandra_tables(instant_status_obj['sample_point'], tables,
                                       event_name='instant_status_resp',
                                       sample_ts=cassandra_time)
