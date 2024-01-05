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
import random

import allure
import json
import pytest
import time

from utils import time_parse
from utils.assertions import assert_equal
from utils.commonlib import show_json


class TestReissue(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, env, cassandra):
        evm_message_in_cassandra = {}
        vin = env['vehicles']['sh_private']['vin']
        vid = env['vehicles']['sh_private']['vehicle_id']
        # platform = mysql['rvs'].fetch('vehicle_platform_config', {"vin": vin})['platform']
        dictionary = {}
        platform = [156]
        # jenkins时区为utc，而本地为北京时区
        # now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H')
        insert_date = time_parse.utc_to_local(offset_hour=8)
        for platform_id in platform:
            evm_message_in_cassandra = cassandra['datacollection'].fetch('evm_message',
                                                                         {'vin': vin,
                                                                          'insert_date': insert_date,
                                                                          'attribution': platform_id})
            dictionary[platform_id] = {
                'vin': vin,
                'vid': vid,
                'len_cassandra': len(evm_message_in_cassandra)
            }
        return dictionary

    def test_reissue_data_nation(self, checker, prepare, publish_msg_by_kafka):
        platform_id = 156
        event_name = 'periodical_journey_update'
        # 车辆信息
        domain = checker.mysql.fetch('vehicle_platform_activated', {"vin": prepare[platform_id]['vin']})[0]['domain']

        # 上报补发消息
        reissue = True
        nextev_message, obj = publish_msg_by_kafka(event_name, vin=prepare[platform_id]['vin'],
                                                   vid=prepare[platform_id]['vid'], reissue=reissue,
                                                   sample_points=[{"vehicle_status":
                                                                       {"mileage": random.randint(0, 999999),
                                                                        "speed": random.randint(0, 220),
                                                                        "vehl_totl_curnt": round(random.uniform(0, 2000), 1)}}])
        # 校验Cassandra
        with allure.step("校验Cassandra收到了evm_server转发的数据"):
            time.sleep(10)
            insert_date = time_parse.utc_to_local(timestamp=time.time(), offset_hour=8)
            # start事件中，Cassandra里的samlpeTs并不是上报消息的sample_ts，MySQL中的sample_time为Cassandra的sampleTs
            gb_evm_message_in_cassandra = checker.cassandra.fetch('evm_message', {'vin': prepare[platform_id]['vin'],
                                                                                  'insert_date': insert_date,
                                                                                  'attribution': platform_id})
            assert_equal(len(gb_evm_message_in_cassandra), prepare[platform_id]['len_cassandra'] + 1)
            sample_ts = json.loads((gb_evm_message_in_cassandra[-1])['message'])['dataUnit']['sampleTs']
            tables = ['evm_message']
            checker.check_cassandra_tables(obj, tables, event_name, domain=domain, platform=platform_id, sample_ts=sample_ts, reissue=reissue)
        # 校验MySQL
        # with allure.step("校验MySQL收到了evm_server转发的数据"):
        #     tables = ['vehicle_data_mock']
        #     checker.check_mysql_tables(obj, tables, event_name, platform=platform_id, sample_ts=sample_ts//1000, reissue=reissue)

    def test_realtime_become_reissue_after_5s(self, checker, prepare, publish_msg_by_kafka):
        platform_id = 156
        event_name = 'periodical_journey_update'
        # 车辆信息
        domain = checker.mysql.fetch('vehicle_platform_activated', {"vin": prepare[platform_id]['vin']})[0]['domain']

        # 上报实时消息
        reissue = False
        nextev_message, obj = publish_msg_by_kafka(event_name, vin=prepare[platform_id]['vin'],
                                                   vid=prepare[platform_id]['vid'], reissue=reissue,
                                                   sample_points=[{"sample_ts": int(round((time.time()-6) * 1000)),
                                                                   "vehicle_status":
                                                                       {"mileage": random.randint(0, 999999),
                                                                        "speed": random.randint(0, 220),
                                                                        "vehl_totl_curnt": round(random.uniform(0, 2000), 1)}}])
        # 校验Cassandra
        with allure.step("校验Cassandra中的commandId为3，表示补发数据"):
            time.sleep(10)
            insert_date = time_parse.utc_to_local(timestamp=time.time(), offset_hour=8)
            # start事件中，Cassandra里的samlpeTs并不是上报消息的sample_ts，MySQL中的sample_time为Cassandra的sampleTs
            gb_evm_message_in_cassandra = checker.cassandra.fetch('evm_message', {'vin': prepare[platform_id]['vin'],
                                                                                  'insert_date': insert_date,
                                                                                  'attribution': platform_id})
            assert_equal(len(gb_evm_message_in_cassandra), prepare[platform_id]['len_cassandra'] + 1)
            sample_ts = json.loads((gb_evm_message_in_cassandra[-1])['message'])['dataUnit']['sampleTs']
            tables = ['evm_message']
            checker.check_cassandra_tables(obj, tables, event_name, domain=domain, platform=platform_id, sample_ts=sample_ts, reissue=True)
        # 校验MySQL
        # with allure.step("校验MySQL中的commandId为3，表示补发数据"):
        #     tables = ['vehicle_data_mock']
        #     checker.check_mysql_tables(obj, tables, event_name, platform=platform_id, sample_ts=sample_ts//1000, reissue=True)
