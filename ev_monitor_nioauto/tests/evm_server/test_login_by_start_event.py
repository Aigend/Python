#!/usr/bin/env python
# coding=utf-8

"""
@author: chunming.liu
@Date: 2019/1/17 <br/>
@Feature: 1)存在于vehicle_profile表、存在于vehicle_platform_config表的私人领域车，给国家平台和地方平台发送车辆login消息（不包含位置数据）
          2)收到mock server 的success ack 后Cassandra表中ack字段变为1<br/>
"""
import datetime
import json
import time

import allure
import pytest

from utils import time_parse
from utils.assertions import assert_equal


class TestVehicleLogin(object):
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
                                                                          'type': 1,
                                                                          'attribution': platform_id})
            dictionary[platform_id] = {
                'vin': vin,
                'vid': vid,
                'len_cassandra': len(evm_message_in_cassandra)
            }
        return dictionary

    @pytest.mark.parametrize("event_name", ['charge_start_event', 'journey_start_event'])
    def test_start_to_login_nation(self, event_name, checker, prepare, publish_msg_by_kafka):
        platform_id = 156
        # 车辆信息
        domain = checker.mysql.fetch('vehicle_platform_activated', {"vin": prepare[platform_id]['vin']})[0]['domain']

        # 上报
        nextev_message, obj = publish_msg_by_kafka(event_name, vin=prepare[platform_id]['vin'], vid=prepare[platform_id]['vid'])

        # 校验Cassandra
        with allure.step("校验Cassandra收到了evm_server转发的数据"):
            time.sleep(5)
            insert_date = time_parse.utc_to_local(timestamp=obj['sample_ts']/1000.0, offset_hour=8)
            # start事件中，Cassandra里的samlpeTs并不是上报消息的sample_ts，MySQL中的sample_time为Cassandra的sampleTs
            gb_evm_message_in_cassandra = checker.cassandra.fetch('evm_message', {'vin': prepare[platform_id]['vin'],
                                                                                  'insert_date': insert_date,
                                                                                  'type': 1,
                                                                                  'attribution': platform_id})
            assert_equal(len(gb_evm_message_in_cassandra), prepare[platform_id]['len_cassandra'] + 1)
            sample_ts = json.loads((gb_evm_message_in_cassandra[-1])['message'])['dataUnit']['sampleTs']//1000
            tables = ['evm_message']
            checker.check_cassandra_tables(obj, tables, event_name, domain=domain, platform=platform_id)
        # 校验MySQL
        # with allure.step("校验MySQL收到了evm_server转发的数据"):
        #     tables = ['vehicle_data_mock']
        #     checker.check_mysql_tables(obj, tables, event_name, platform=platform_id, sample_ts=sample_ts)
