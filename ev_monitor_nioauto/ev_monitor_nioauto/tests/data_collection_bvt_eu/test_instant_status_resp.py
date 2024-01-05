#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:kangkai.cao
@time: 2021/11/03
@api: GET_/api/XXX 【必填】
@showdoc: XXX
@description: 脚本描述
"""

import pytest
import time
import allure
from utils.time_parse import timestamp_to_utc_strtime

list_situation = (True,)
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
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    @pytest.mark.parametrize("set_outside_sample_ts", list_situation, ids=case)
    def test_instant_status_resp(self, vid, kafka, prepare, checker, publish_msg, set_outside_sample_ts):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1
        if set_outside_sample_ts:
            nextev_message, instant_status_obj = publish_msg('instant_status_resp', platform_type=1,
                                                             outside_sample_ts=int(round(time.time() * 1000)),
                                                             sample_point={
                                                                 "vehicle_status": {
                                                                     "mileage": mileage}
                                                             })
        else:
            nextev_message, instant_status_obj = publish_msg('instant_status_resp', sleep_time=30, platform_type=1,
                                                             sample_point={
                                                                 "vehicle_status": {
                                                                     "mileage": mileage}
                                                             })

        # 校验cassandra
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
                                   # 'btry_pak_info',
                                   # 're_alarm_data',
                                   'alarm_data',
                                   'evm_flag',
                                   'sample_ts']
                  }
        instant_status_obj['sample_point'].pop('battery_package_info')
        # 目前stg_eu的cassandra还没上线这俩个字段，失败处理
        # instant_status_obj['sample_point']['driving_data'].pop('veh_dispd_spd')
        # instant_status_obj['sample_point']['driving_data'].pop('veh_outd_hum')
        checker.check_cassandra_tables(instant_status_obj['sample_point'], tables,
                                       event_name='instant_status_resp',
                                       sample_ts=cassandra_time)

        # 校验mysql
        tables = ['status_position', 'status_vehicle', 'status_soc',
                  'status_btry_packs', 'status_occupant', 'status_driving_motor',
                  'status_extremum_data', 'status_driving_data', 'status_hvac',
                  'status_tyre', 'status_door', 'status_light', 'status_window']

        for table in tables:
            assert len(checker.mysql.fetch(table, {'id': vid, 'sample_time': timestamp_to_utc_strtime(cassandra_time)},
                                           fields=['id'])) == 1
