#!/usr/bin/env python
# coding=utf-8

"""
@author: chunming.liu
@Date: 2019/1/17
@Feature: 1)存在于vehicle_profile表、存在于vehicle_platform_config表的私人领域车，给国家平台和地方平台发送车辆实时消息（包括evm故障信息，如有）
          2）给国家和地方平台发送的数据中，包括整车数据vehicle_status\驱动电机driving_motor\极值extremum\报警alarm，不包含位置数据
          3)收到mock server 的success ack 后Cassandra表中ack字段变为1<br/>
          4)如果车辆离线，发送实时消息前，evm_server主动给国家和地方平台发送一个车辆login消息
          5)如果要给国家传报警数据，要在vehicle_platform_activated表中，将alarm_enable字段设成NULL或者1，并且status=1.
"""
import datetime
import json
import random

import allure
import pytest
import time

from utils import time_parse, message_formator
from utils.assertions import assert_equal


class TestPublicRealtime(object):
    @pytest.mark.parametrize("event_name", ['periodical_journey_update', 'periodical_charge_update'])
    def test_public_realtime_nation(self, event_name, checker, env, publish_msg_by_kafka, cassandra, cmdopt):
        # 车辆信息
        vin = env['vehicles']['sh_public']['vin']
        vid = env['vehicles']['sh_public']['vehicle_id']
        platform_id = 156
        domain = checker.mysql.fetch('vehicle_platform_activated', {"vin": vin})[0]['domain']

        # 消息上报
        # 注意：evm上报的数据有效范围与我们自己定义的有效范围不尽相同
        nextev_message, obj = publish_msg_by_kafka(event_name, vin=vin, vid=vid,
                                                   sample_points=[{"vehicle_status":
                                                                       {"mileage": random.randint(0, 999999),
                                                                        "speed": random.randint(0, 220),
                                                                        "vehl_totl_curnt": round(random.uniform(0, 2000), 1)}}])
        # 校验Cassandra
        with allure.step("校验Cassandra收到了evm_server转发的数据"):
            insert_date = time_parse.utc_to_local(timestamp=time.time(), offset_hour=8)
            # start事件中，Cassandra里的samlpeTs并不是上报消息的sample_ts，MySQL中的sample_time为Cassandra的sampleTs
            sample_ts = obj['sample_points'][0]['sample_ts']
            for i in range(20):
                time.sleep(1)
                gb_evm_message_in_cassandra = cassandra['datacollection'].fetch('evm_message',
                                                                                {"vin": vin,
                                                                                 "insert_date": insert_date,
                                                                                 'sample_ts': sample_ts,
                                                                                 "attribution": platform_id})
                if len(gb_evm_message_in_cassandra) == 1:
                    break
            sample_ts = json.loads((gb_evm_message_in_cassandra[-1])['message'])['dataUnit']['sampleTs']
            tables = ['evm_message']
            checker.check_cassandra_tables(obj, tables, event_name, domain=domain, platform=platform_id, sample_ts=sample_ts)
        # 校验MySQL
        with allure.step("校验MySQL收到了evm_server转发的数据"):
            if cmdopt == 'test':
                tables = ['vehicle_data_mock']
                checker.check_mysql_tables(obj, tables, event_name, platform=platform_id, sample_ts=sample_ts // 1000)

    @pytest.mark.parametrize("event_name", ['periodical_journey_update', 'periodical_charge_update'])
    def test_update_status_4_to_3_nation(self, event_name, checker, env, publish_msg_by_kafka, cassandra, cmdopt):
        # 车辆信息
        vin = env['vehicles']['sh_public']['vin']
        vid = env['vehicles']['sh_public']['vehicle_id']
        platform_id = 156
        domain = checker.mysql.fetch('vehicle_platform_activated', {"vin": vin})[0]['domain']

        # 消息上报
        # 注意：evm上报的数据有效范围与我们自己定义的有效范围不尽相同
        nextev_message, obj = publish_msg_by_kafka(event_name, vin=vin, vid=vid,
                                                   sample_points=[{"vehicle_status":
                                                                       {"mileage": random.randint(0, 999999),
                                                                        "speed": random.randint(0, 220),
                                                                        "vehl_totl_curnt": round(random.uniform(0, 2000), 1),
                                                                        "vehl_state": 4}}])
        sample_ts = obj['sample_points'][0]['sample_ts']

        # 校验Cassandra
        with allure.step("校验{0}存入Cassandra的{1}".format(event_name, 'evm_message')):
            insert_date = time_parse.utc_to_local(timestamp=sample_ts / 1000.0, offset_hour=8)
            for i in range(20):
                time.sleep(1)
                gb_evm_message_in_cassandra = cassandra['datacollection'].fetch('evm_message',
                                                                                {"vin": vin,
                                                                                 "insert_date": insert_date,
                                                                                 'sample_ts': sample_ts,
                                                                                 "attribution": platform_id})
                if len(gb_evm_message_in_cassandra) == 1:
                    event_in_cassandra = gb_evm_message_in_cassandra[0]
                    break
            evm_event_in_cassandra = {
                "vin": event_in_cassandra['vin'],
                "attribution": event_in_cassandra['attribution'],
                "ack": event_in_cassandra['ack'],
                "domain": event_in_cassandra['domain'],
                "type": event_in_cassandra['type']
            }
            cassandra_formator = message_formator.MsgToCassandraFormator(obj['id'], sample_ts)
            obj_to_evm_message = cassandra_formator.to_evm_message(obj, event_name, domain, platform_id)
            # 校验evm头部
            assert_equal(evm_event_in_cassandra, obj_to_evm_message)
            # 校验消息体内的vehicleState字段
            message_in_cassandra = json.loads(event_in_cassandra['message'])
            dataUnit_in_cassandra = message_in_cassandra['dataUnit']['reportInfoList']
            assert_equal(dataUnit_in_cassandra[0]['infoBody']['vehicleState'], 3)
        # 校验MySQL
        with allure.step("校验 evm_message 信息存入Mysql的 vehicle_data_mock 表"):
            if cmdopt != 'test':
                return
            sample_time = time_parse.time_sec_to_strtime(sample_ts // 1000)
            vehicle_data_mock_in_mysql = checker.mysql.fetch('vehicle_data_mock',
                                                             {"vin": obj['id'],
                                                              "sample_time": sample_time},
                                                             exclude_fields=['id', 'sample_time', 'update_time'])[-1]
            evm_vehicle_data_mock_in_mysql = {"vin": vehicle_data_mock_in_mysql['vin'],
                                              "command": vehicle_data_mock_in_mysql['command'],
                                              "attribution": vehicle_data_mock_in_mysql['attribution']}

            formator = message_formator.MessageFormator(obj['id'], sample_ts // 1000)
            mock_in_message = formator.to_mysql_vehicle_data_mock(obj, platform_id, event_name)
            # 校验evm头部
            assert_equal(evm_vehicle_data_mock_in_mysql, mock_in_message)
            # 校验消息体内的vehicleState字段
            message_in_mysql = json.loads(vehicle_data_mock_in_mysql['message'])
            dataUnit_in_mysql = message_in_mysql['dataUnit']['reportInfoList']
            assert_equal(dataUnit_in_mysql[0]['infoBody']['vehicleState'], 3)
