#!/usr/bin/env python
# coding=utf-8

"""
:file: test_charge_start_event.py
:author: chunming.liu
:Date: Created on 2019/11/11
:Description: 充电开始事件，包含电池数据
"""
import datetime
import allure
import pytest
from utils.assertions import assert_equal
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestChargeStartMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_charge_start_event(self, publish_msg, checker, prepare, vid, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1
        nextev_message, charge_start_obj = publish_msg('charge_start_event',
                                                       vehicle_status={"mileage": mileage})

        # 校验cassandra
        tables = {
            'vehicle_data': ['vehicle_id',
                             'charging_info',
                             'soc_status',
                             'position_status',
                             'vehicle_status',
                             'btry_pak_info', #马可波罗环境不存储bid，电池编码截断
                             'icc_id',
                             'process_id as charge_id',
                             'sample_ts'],

            # 'driving_data': ['dump_enrgy',
            #                  'mileage',
            #                  'position',
            #                  'posng_valid_type',
            #                  'soc',
            #                  'speed',
            #                  'realtime_power_consumption',
            #                  'sample_ts']
        }
        checker.check_cassandra_tables(charge_start_obj, tables, event_name='charge_start_event')

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=30):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == charge_start_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        # 新增bid字段，验证推送到大数据平台的消息里携带
        # assert 'bid' in msg['params']['vehicle_status']['battery_package_info']['btry_pak_encoding'][0]
        # msg['params']['vehicle_status']['battery_package_info']['btry_pak_encoding'][0].pop('bid')
        # msg['params']['original_length'] = str(int(msg['params']['original_length'])-34)
        #
        # with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
        #     assert_equal(msg, parse_nextev_message(nextev_message))

        # 校验mysql
        tables = ['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs']

        checker.check_mysql_tables(charge_start_obj, tables, event_name='charge_start_event')

        # 校验mongo，访问mongo需用欧洲堡垒机，欧洲堡垒机只能申请临时权限
        collections = ['vehicle_position']
        checker.check_mongodb_collections(charge_start_obj, collections, event_name='charge_start_event', sample_ts=charge_start_obj['sample_ts'])
