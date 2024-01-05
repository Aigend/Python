#!/usr/bin/env python
# coding=utf-8

"""
@author: chunming.liu
@Date: 2019/1/17
@Feature: 1)存在于vehicle_profile表、存在于vehicle_platform_config表的私人领域车，给国家平台和地方平台发送车辆实时消息（包括evm故障信息，如有）
          2）给国家和地方平台发送的数据中，包括整车数据vehicle_status\驱动电机driving_motor\极值extremum\报警alarm，
            platform_config不包含位置数据
          3)收到mock server 的success ack 后Cassandra表中ack字段变为1<br/>
          4)如果车辆离线，发送实时消息前，evm_server主动给国家和地方平台发送一个车辆login消息
          5)如果要给国家传报警数据，要在vehicle_platform_activated表中，将alarm_enable字段设成NULL或者1，并且status=1.
"""
import datetime
import random
import json

import allure
import pytest
import time

from utils import time_parse
from utils.assertions import assert_equal
from utils.time_parse import time_sec_to_strtime


class TestRealTime(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, env, cassandra, mysql, request):
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

        # 修改国家平台配置为不上报私家车的位置信息，代码运行完后恢复原有配置
        orig_private_gps_mysql = mysql['vms'].fetch('platform_config',
                                                    {"area_code": 156,
                                                     "domain": 2},
                                                    fields=['private_gps'])[0]['private_gps']
        mysql['vms'].update('platform_config',
                            where_model={"area_code": 156,
                                         "domain": 2},
                            fields_with_data={"private_gps": 2})

        def fin():
            mysql['vms'].update('platform_config',
                                where_model={"area_code": 156,
                                             "domain": 2},
                                fields_with_data={"area_code": 156,
                                                  "private_gps": orig_private_gps_mysql})

        request.addfinalizer(fin)

        return dictionary

    # @pytest.mark.parametrize("event_name", ['periodical_journey_update', 'periodical_charge_update'])
    @pytest.mark.skip('Manual')
    def test_private_realtime_nation(self, event_name, checker, prepare, publish_msg_by_kafka):
        # 更改数据库之后需要一定的时间才能生效
        time.sleep(30)

        # 车辆信息
        platform_id = 156
        domain = checker.mysql.fetch('vehicle_platform_activated', {"vin": prepare[platform_id]['vin']})[0]['domain']

        # 上报
        nextev_message, obj = publish_msg_by_kafka(event_name, vin=prepare[platform_id]['vin'],
                                                   vid=prepare[platform_id]['vid'],
                                                   sample_points=[{"vehicle_status":
                                                                       {"mileage": random.randint(0, 999999),
                                                                        "speed": random.randint(0, 220),
                                                                        "vehl_totl_curnt": round(random.uniform(0, 2000), 1)}}])

        with allure.step("校验私有车辆不上报GPS"):
            insert_date = time_parse.utc_to_local(timestamp=time.time(), offset_hour=8)
            # start事件中，Cassandra里的samlpeTs并不是上报消息的sample_ts，MySQL中的sample_time为Cassandra的sampleTs
            gb_evm_message_in_cassandra = checker.cassandra.fetch('evm_message', {'vin': prepare[platform_id]['vin'],
                                                                                  'insert_date': insert_date,
                                                                                  'attribution': platform_id})
            assert_equal(len(gb_evm_message_in_cassandra), prepare[platform_id]['len_cassandra'] + 1)
            sample_ts = json.loads((gb_evm_message_in_cassandra[-1])['message'])['dataUnit']['sampleTs']
            # 校验私有车辆不上报GPS
            assert "positionState" and "longitude" and "latitude" not in gb_evm_message_in_cassandra[-1]['message']
        # 校验Cassandra
        with allure.step("校验Cassandra收到了evm_server转发的数据"):
            tables = ['evm_message']
            checker.check_cassandra_tables(obj, tables, event_name, domain=domain, platform=platform_id, sample_ts=sample_ts)
        # 校验MySQL
        with allure.step("校验MySQL收到了evm_server转发的数据"):
            tables = ['vehicle_data_mock']
            checker.check_mysql_tables(obj, tables, event_name, platform=platform_id, sample_ts=sample_ts // 1000)

    @pytest.mark.skip('Manual')
    def test_private_realtime_nation_manual(self, publish_msg_by_kafka):
        """
        update数据库可能会出现未及时更新的问题，需手工校验
        1、VMS政府平台配置页面中修改"国家""私有"平台中私有领域GPS为不上报
        2、publish私有车辆'periodical_journey_update', 'periodical_charge_update'到国家平台
        3、校验Cassandra中对应记录，无"positionState"、"longitude"和"latitude"字段
        4、校验Cassandra和mysql中"ack"=1、"command"=2、"platform"=156、"domain"=2等字段
        """
        pass

    @pytest.mark.skip('Manual')
    @pytest.mark.parametrize("event_name", ['periodical_journey_update', 'periodical_charge_update'])
    def test_vehl_totl_curnt_nation(self, event_name, checker, prepare, publish_msg_by_kafka):
        """
        vehl_totl_curnt值在[-3000,3000]时，校验上mock server那边所存的值为(value+1000)*10
        值超出[-3000,3000]的范围时，会被置为65534

        known issue:目前如果vehl_totl_curnt在[-3000,-1000)时，mock_server的值的运算规则目前不符合(value+1000)*10

        """
        # 车辆信息
        platform_id = 156
        domain = checker.mysql.fetch('vehicle_platform_activated', {"vin": prepare[platform_id]['vin']})[0]['domain']

        # 上报
        nextev_message, obj = publish_msg_by_kafka(event_name=event_name,
                                                   vin=prepare[platform_id]['vin'],
                                                   vid=prepare[platform_id]['vid'],
                                                   sample_points=[{"vehicle_status": {"vehl_totl_curnt": 2000.0}}])
        # 校验mysql
        time.sleep(10)
        sample_time = time_sec_to_strtime(obj['sample_points'][0]['sample_ts'] // 1000)
        gb_mock_all = checker.mysql.fetch('vehicle_data_mock',
                                          {"vin": prepare[platform_id]['vin'],
                                           "sample_time": sample_time,
                                           "attribution": platform_id})[-1]

        gb_mock_msg = json.loads(gb_mock_all['message'])
        vehl_totl_curnt_in_msg = obj['sample_points'][0]['vehicle_status']['vehl_totl_curnt']
        vehl_totl_curnt_in_msg_format = int((round(vehl_totl_curnt_in_msg, 1) + 1000) * 10)
        vehl_totl_curnt_in_mysql = gb_mock_msg['dataUnit']['reportInfoList'][0]['infoBody']['vehicleTotalCurrent']
        assert_equal(vehl_totl_curnt_in_mysql, vehl_totl_curnt_in_msg_format)
