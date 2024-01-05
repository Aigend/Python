#!/usr/bin/env python
# coding=utf-8

"""
@author: chunming.liu
@Date: 2019/1/17 <br/>
@Feature: 1)存在于vehicle_profile表、存在于vehicle_platform_config表的私人领域车，给国家平台和地方平台发送AlarmSignal中的EVM类alarm
          2）vehicle_platform_activated表中alarm_enable字段设成NULL或者1,会转发alarm给国家平台和地方平台
          3）vehicle_platform_activated表中alarm_enable字段设成其他值,不会转发alarm给国家平台和地方平台
          4）如果上报的消息中包含alarm_data（老协议），会优先使用这里面的EVM alarm数据发给国家平台和地方平台，而忽略AlarmSignal中的。
          5)上报国家平台的只有charge/journey周期update事件
          6)只有update事件上报evm范围内的alarm_signal，并且vehicle_platform_activated表中alarm_enable=1时才会把数据上报国家平台
"""
import datetime
import time
import random

import allure
import json
import pytest
from nio_messages.wti import EVM_WTI_SIGNAL
from utils import time_parse
from utils.assertions import assert_equal
from utils.commonlib import show_json
from utils.time_parse import time_sec_to_strtime

index_names = ['WTI-BMS-8', 'WTI-EP-15', 'WTI-BC-1', 'WTI-BC-10', 'WTI-PBRK-6', 'WTI-VSTB-2', 'WTI-BC-4']


class TestAlarm(object):
    def test_alarm_signal_nation(self, env, mysql, cassandra, publish_msg_by_kafka):
        # 国家平台
        platform_id = 156
        vin = env['vehicles']['sh_private']['vin']
        vid = env['vehicles']['sh_private']['vehicle_id']
        # 上报
        signal_int = random.choice(EVM_WTI_SIGNAL)
        alarm_level = signal_int['evm_alarm_level']
        alarm_code = signal_int['alarm_code']
        nextev_message, charge_update_obj = publish_msg_by_kafka('periodical_charge_update',
                                                                 vin=vin,
                                                                 vid=vid,
                                                                 sample_points=[{
                                                                     "alarm_signal": {"signal_int": [signal_int]}}],
                                                                 clear_fields=["sample_points[0].alarm_data"])
        # 校验Cassandra
        with allure.step("校验Cassandra收到了转发报警的数据"):
            insert_date = time_parse.utc_to_local(timestamp=charge_update_obj['sample_points'][0]['sample_ts'] / 1000.0, offset_hour=8)
            sample_ts = charge_update_obj['sample_points'][0]['sample_ts']
            for i in range(20):
                time.sleep(1)
                gb_evm_message_in_cassandra = cassandra['datacollection'].fetch('evm_message',
                                                                                {"vin": vin,
                                                                                 "insert_date": insert_date,
                                                                                 'sample_ts': sample_ts,
                                                                                 "attribution": platform_id})
                if len(gb_evm_message_in_cassandra) == 1:
                    break

            allure.attach(show_json(gb_evm_message_in_cassandra[-1]), "mock_server收到的内容")
            message_in_cassandra = json.loads(gb_evm_message_in_cassandra[-1]['message'])
            assert_equal(message_in_cassandra['uniqueId'], vin)
            assert_equal(message_in_cassandra['command'], 2)  # 表示实时消息
            assert_equal(message_in_cassandra['ack'], 254)
            assert_equal(message_in_cassandra['dataUnit']['sampleTs'], charge_update_obj['sample_points'][0]['sample_ts'])
            assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'], alarm_level)
            # 向左挪几位参见https://git.nevint.com/greatwall/evm_server/blob/master/src/main/profiles/wti_signal.json中的alarm_code
            assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], 1 << alarm_code)

        # 校验mysql
        # with allure.step("校验MySQL收到了转发报警的数据"):
        #     sample_time = time_sec_to_strtime(charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        #     gb_evm_message_in_mysql = mysql['rvs'].fetch('vehicle_data_mock',
        #                                                  {"vin": prepare[platform_id]['vin'],
        #                                                   "sample_time": sample_time,
        #                                                   "command": 2,
        #                                                   "attribution": platform_id})[0]
        #
        #     allure.attach(show_json(gb_evm_message_in_mysql), "mock_server收到的内容")
        #     message_in_mysql = json.loads(gb_evm_message_in_mysql['message'])
        #     assert_equal(message_in_mysql['uniqueId'], prepare[platform_id]['vin'])
        #     assert_equal(message_in_mysql['commandId'], 2)  # 表示实时消息
        #     assert_equal(message_in_mysql['ack'], 254)
        #     assert_equal(message_in_mysql['dataUnit']['sampleTs'], charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        #     assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'], alarm_level)
        #     # 向左挪几位参见https://git.nevint.com/greatwall/evm_server/blob/master/src/main/profiles/wti_signal.json中的alarm_code
        #     assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], 1 << alarm_code)

    def test_WTI_EVM_20(self, env, mysql, cassandra, publish_msg_by_kafka):
        # 国家平台
        platform_id = 156
        vin = env['vehicles']['sh_private']['vin']
        vid = env['vehicles']['sh_private']['vehicle_id']
        # 上报
        signal_int = {'name': 'BMSDCChargeCurrentOverUnder', 'value': 1, 'alarm_level': 1, 'evm_alarm_level': 3, 'alarm_code': 18, 'wti_code': 'WTI-EVM-20',
                      'note': 'ProtoBufVersion>=16且BMSDCChargeCurrentOverUnder=1，只生成WTI-BMS-10，ProtoBufVersion<16且BMSDCChargeCurrentOverUnder=1，生成WTI-BMS-10和WTI-EVM-20'}
        alarm_level = signal_int['evm_alarm_level']
        alarm_code = signal_int['alarm_code']
        # 修改ProtoBufVersion<16
        nextev_message, charge_update_obj = publish_msg_by_kafka('periodical_charge_update', protobuf_v=15,
                                                                 vin=vin,
                                                                 vid=vid,
                                                                 sample_points=[{
                                                                     "alarm_signal": {"signal_int": [signal_int]}}],
                                                                 clear_fields=["sample_points[0].alarm_data"])
        # 校验Cassandra
        with allure.step("校验Cassandra收到了转发报警的数据"):
            insert_date = time_parse.utc_to_local(timestamp=charge_update_obj['sample_points'][0]['sample_ts'] / 1000.0, offset_hour=8)
            sample_ts = charge_update_obj['sample_points'][0]['sample_ts']
            for i in range(20):
                time.sleep(1)
                gb_evm_message_in_cassandra = cassandra['datacollection'].fetch('evm_message',
                                                                                {"vin": vin,
                                                                                 "insert_date": insert_date,
                                                                                 'sample_ts': sample_ts,
                                                                                 "attribution": platform_id})
                if len(gb_evm_message_in_cassandra) == 1:
                    break
            allure.attach(show_json(gb_evm_message_in_cassandra[-1]), "mock_server收到的内容")
            message_in_cassandra = json.loads(gb_evm_message_in_cassandra[-1]['message'])
            assert_equal(message_in_cassandra['uniqueId'], vin)
            assert_equal(message_in_cassandra['command'], 2)  # 表示实时消息
            assert_equal(message_in_cassandra['ack'], 254)
            assert_equal(message_in_cassandra['dataUnit']['sampleTs'], charge_update_obj['sample_points'][0]['sample_ts'])
            assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'], alarm_level)
            # 向左挪几位参见https://git.nevint.com/greatwall/evm_server/blob/master/src/main/profiles/wti_signal.json中的alarm_code
            assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], 1 << alarm_code)

        # 校验mysql
        # with allure.step("校验MySQL收到了转发报警的数据"):
        #     sample_time = time_sec_to_strtime(charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        #     gb_evm_message_in_mysql = mysql['rvs'].fetch('vehicle_data_mock',
        #                                                  {"vin": prepare[platform_id]['vin'],
        #                                                   "sample_time": sample_time,
        #                                                   "command": 2,
        #                                                   "attribution": platform_id})[0]
        #
        #     allure.attach(show_json(gb_evm_message_in_mysql), "mock_server收到的内容")
        #     message_in_mysql = json.loads(gb_evm_message_in_mysql['message'])
        #     assert_equal(message_in_mysql['uniqueId'], prepare[platform_id]['vin'])
        #     assert_equal(message_in_mysql['commandId'], 2)  # 表示实时消息
        #     assert_equal(message_in_mysql['ack'], 254)
        #     assert_equal(message_in_mysql['dataUnit']['sampleTs'], charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        #     assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'], alarm_level)
        #     # 向左挪几位参见https://git.nevint.com/greatwall/evm_server/blob/master/src/main/profiles/wti_signal.json中的alarm_code
        #     assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], 1 << alarm_code)

    @pytest.mark.parametrize("signal_name", index_names)
    def test_alarm_signal_nation_by_index(self, env, mysql, cassandra, signal_name, publish_msg_by_kafka):
        # 国家平台
        platform_id = 156
        vin = env['vehicles']['sh_private']['vin']
        vid = env['vehicles']['sh_private']['vehicle_id']
        # 上报
        signal_int = list(filter(lambda x: x['name'] == signal_name, EVM_WTI_SIGNAL))[0]
        alarm_level = signal_int['evm_alarm_level']
        alarm_code = signal_int['alarm_code']
        nextev_message, charge_update_obj = publish_msg_by_kafka('periodical_charge_update',
                                                                 vin=vin,
                                                                 vid=vid,
                                                                 sample_points=[{
                                                                     "alarm_signal": {"signal_int": [signal_int]}}],
                                                                 clear_fields=["sample_points[0].alarm_data"])
        # 校验Cassandra
        with allure.step("校验Cassandra收到了转发报警的数据"):
            insert_date = time_parse.utc_to_local(timestamp=charge_update_obj['sample_points'][0]['sample_ts'] / 1000.0, offset_hour=8)
            sample_ts = charge_update_obj['sample_points'][0]['sample_ts']
            for i in range(20):
                time.sleep(1)
                gb_evm_message_in_cassandra = cassandra['datacollection'].fetch('evm_message',
                                                                                {"vin": vin,
                                                                                 "insert_date": insert_date,
                                                                                 'sample_ts': sample_ts,
                                                                                 "attribution": platform_id})
                if len(gb_evm_message_in_cassandra) == 1:
                    break

            allure.attach(show_json(gb_evm_message_in_cassandra[-1]), "mock_server收到的内容")
            message_in_cassandra = json.loads(gb_evm_message_in_cassandra[-1]['message'])
            assert_equal(message_in_cassandra['uniqueId'], vin)
            assert_equal(message_in_cassandra['command'], 2)  # 表示实时消息
            assert_equal(message_in_cassandra['ack'], 254)
            assert_equal(message_in_cassandra['dataUnit']['sampleTs'], charge_update_obj['sample_points'][0]['sample_ts'])
            assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'], alarm_level)
            # 向左挪几位参见https://git.nevint.com/greatwall/evm_server/blob/master/src/main/profiles/wti_signal.json中的alarm_code
            assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], 1 << alarm_code)

        # 校验mysql
        # with allure.step("校验MySQL收到了转发报警的数据"):
        #     sample_time = time_sec_to_strtime(charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        #     gb_evm_message_in_mysql = mysql['rvs'].fetch('vehicle_data_mock',
        #                                                  {"vin": prepare[platform_id]['vin'],
        #                                                   "sample_time": sample_time,
        #                                                   "command": 2,
        #                                                   "attribution": platform_id})[0]
        #
        #     allure.attach(show_json(gb_evm_message_in_mysql), "mock_server收到的内容")
        #     message_in_mysql = json.loads(gb_evm_message_in_mysql['message'])
        #     assert_equal(message_in_mysql['uniqueId'], prepare[platform_id]['vin'])
        #     assert_equal(message_in_mysql['commandId'], 2)  # 表示实时消息
        #     assert_equal(message_in_mysql['ack'], 254)
        #     assert_equal(message_in_mysql['dataUnit']['sampleTs'], charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        #     assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'], alarm_level)
        #     # 向左挪几位参见https://git.nevint.com/greatwall/evm_server/blob/master/src/main/profiles/wti_signal.json中的alarm_code
        #     assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], 1 << alarm_code)

    @pytest.mark.parametrize("signal_int", list(filter(lambda x: 'note' in x and '轻量级' in x['note'], EVM_WTI_SIGNAL)))
    def test_slight_alarm_signals(self, env, mysql, cassandra, signal_int, publish_msg_by_kafka):
        # 国家平台
        platform_id = 156
        vin = env['vehicles']['sh_private']['vin']
        vid = env['vehicles']['sh_private']['vehicle_id']
        # 上报
        alarm_level = signal_int['evm_alarm_level']
        alarm_code = signal_int['alarm_code']
        nextev_message, charge_update_obj = publish_msg_by_kafka('periodical_charge_update',
                                                                 vin=vin,
                                                                 vid=vid,
                                                                 sample_points=[{
                                                                    "alarm_signal": {"signal_int": [signal_int]}}],
                                                                    clear_fields=["sample_points[0].alarm_data"])
        # 校验Cassandra
        with allure.step("校验Cassandra收到了转发报警的数据"):
            insert_date = time_parse.utc_to_local(timestamp=charge_update_obj['sample_points'][0]['sample_ts'] / 1000.0, offset_hour=8)
            sample_ts = charge_update_obj['sample_points'][0]['sample_ts']
            for i in range(20):
                time.sleep(1)
                gb_evm_message_in_cassandra = cassandra['datacollection'].fetch('evm_message',
                                                                                {"vin": vin,
                                                                                 "insert_date": insert_date,
                                                                                 'sample_ts': sample_ts,
                                                                                 "attribution": platform_id})
                if len(gb_evm_message_in_cassandra) == 1:
                    break

            allure.attach(show_json(gb_evm_message_in_cassandra[-1]), "mock_server收到的内容")
            message_in_cassandra = json.loads(gb_evm_message_in_cassandra[-1]['message'])
            assert_equal(message_in_cassandra['uniqueId'], vin)
            assert_equal(message_in_cassandra['command'], 2)  # 表示实时消息
            assert_equal(message_in_cassandra['ack'], 254)
            assert_equal(message_in_cassandra['dataUnit']['sampleTs'], charge_update_obj['sample_points'][0]['sample_ts'])
            assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'], alarm_level)
            # 向左挪几位参见https://git.nevint.com/greatwall/evm_server/blob/master/src/main/profiles/wti_signal.json中的alarm_code
            if signal_int['name'] == 'BatteryCellVolHighAlarm':
                flag = (1 << 18) + (1 << 5)
                assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], flag)
            else:
                assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], 1 << alarm_code)

        # 校验mysql
        # with allure.step("校验MySQL收到了转发报警的数据"):
        #     sample_time = time_sec_to_strtime(charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        #     gb_evm_message_in_mysql = mysql['rvs'].fetch('vehicle_data_mock',
        #                                                  {"vin": prepare[platform_id]['vin'],
        #                                                   "sample_time": sample_time,
        #                                                   "command": 2,
        #                                                   "attribution": platform_id})[0]
        #
        #     allure.attach(show_json(gb_evm_message_in_mysql), "mock_server收到的内容")
        #     message_in_mysql = json.loads(gb_evm_message_in_mysql['message'])
        #     assert_equal(message_in_mysql['uniqueId'], prepare[platform_id]['vin'])
        #     assert_equal(message_in_mysql['commandId'], 2)  # 表示实时消息
        #     assert_equal(message_in_mysql['ack'], 254)
        #     assert_equal(message_in_mysql['dataUnit']['sampleTs'], charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        #     assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'], alarm_level)
        #     # 向左挪几位参见https://git.nevint.com/greatwall/evm_server/blob/master/src/main/profiles/wti_signal.json中的alarm_code
        #     if signal_int['name'] == 'BatteryCellVolHighAlarm':
        #         flag = (1 << 18) + (1 << 5)
        #         assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], flag)
        #     else:
        #         assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], 1 << alarm_code)

    @pytest.mark.parametrize("signal_int", list(filter(lambda x: 'note' in x and '中量级' in x['note'], EVM_WTI_SIGNAL)))
    def test_medium_alarm_signals(self, env, mysql, cassandra, signal_int, publish_msg_by_kafka):
        # 国家平台
        platform_id = 156
        vin = env['vehicles']['sh_private']['vin']
        vid = env['vehicles']['sh_private']['vehicle_id']
        # 上报
        alarm_level = signal_int['evm_alarm_level']
        alarm_code = signal_int['alarm_code']
        nextev_message, charge_update_obj = publish_msg_by_kafka('periodical_charge_update',
                                                                 vin=vin,
                                                                 vid=vid,
                                                                 sample_points=[{
                                                                    "alarm_signal": {"signal_int": [signal_int]}}],
                                                                    clear_fields=["sample_points[0].alarm_data"])
        # 校验Cassandra
        with allure.step("校验Cassandra收到了转发报警的数据"):
            insert_date = time_parse.utc_to_local(timestamp=charge_update_obj['sample_points'][0]['sample_ts'] / 1000.0, offset_hour=8)
            sample_ts = charge_update_obj['sample_points'][0]['sample_ts']
            for i in range(20):
                time.sleep(1)
                gb_evm_message_in_cassandra = cassandra['datacollection'].fetch('evm_message',
                                                                                {"vin": vin,
                                                                                 "insert_date": insert_date,
                                                                                 'sample_ts': sample_ts,
                                                                                 "attribution": platform_id})
                if len(gb_evm_message_in_cassandra) == 1:
                    break

            allure.attach(show_json(gb_evm_message_in_cassandra[-1]), "mock_server收到的内容")
            message_in_cassandra = json.loads(gb_evm_message_in_cassandra[-1]['message'])
            assert_equal(message_in_cassandra['uniqueId'], vin)
            assert_equal(message_in_cassandra['command'], 2)  # 表示实时消息
            assert_equal(message_in_cassandra['ack'], 254)
            assert_equal(message_in_cassandra['dataUnit']['sampleTs'], charge_update_obj['sample_points'][0]['sample_ts'])
            assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'], alarm_level)
            # 向左挪几位参见https://git.nevint.com/greatwall/evm_server/blob/master/src/main/profiles/wti_signal.json中的alarm_code
            if signal_int['name'] == 'BatteryCellVolHighAlarm':
                flag = (1 << 18) + (1 << 5)
                assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], flag)
            else:
                assert_equal(message_in_cassandra['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], 1 << alarm_code)

        # 校验mysql
        # with allure.step("校验MySQL收到了转发报警的数据"):
        #     sample_time = time_sec_to_strtime(charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        #     gb_evm_message_in_mysql = mysql['rvs'].fetch('vehicle_data_mock',
        #                                                  {"vin": prepare[platform_id]['vin'],
        #                                                   "sample_time": sample_time,
        #                                                   "command": 2,
        #                                                   "attribution": platform_id})[0]
        #
        #     allure.attach(show_json(gb_evm_message_in_mysql), "mock_server收到的内容")
        #     message_in_mysql = json.loads(gb_evm_message_in_mysql['message'])
        #     assert_equal(message_in_mysql['uniqueId'], prepare[platform_id]['vin'])
        #     assert_equal(message_in_mysql['commandId'], 2)  # 表示实时消息
        #     assert_equal(message_in_mysql['ack'], 254)
        #     assert_equal(message_in_mysql['dataUnit']['sampleTs'], charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        #     assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'], alarm_level)
        #     # 向左挪几位参见https://git.nevint.com/greatwall/evm_server/blob/master/src/main/profiles/wti_signal.json中的alarm_code
        #     if signal_int['name'] == 'BatteryCellVolHighAlarm':
        #         flag = (1 << 18) + (1 << 5)
        #         assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], flag)
        #     else:
        #         assert_equal(message_in_mysql['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'], 1 << alarm_code)