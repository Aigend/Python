#!/usr/bin/env python
# coding=utf-8
import allure
import pytest
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestChargeEndMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_charge_end_event(self, publish_msg, kafka, checker, vid, prepare):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, charge_end_obj = publish_msg('charge_end_event', sleep_time=30,
                                                     vehicle_status={"mileage": prepare['original_mileage'] + 1})

        # 校验cassandra
        tables ={'vehicle_data':['vehicle_id',
                                 'charging_info',
                                 'soc_status',
                                 'position_status',
                                 'vehicle_status',
                                 'process_id as charge_id',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(charge_end_obj, tables, event_name='charge_end_event')

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == charge_end_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            original_msg = parse_nextev_message(nextev_message)
            original_msg['params']['vehicle_status']['position_status'].pop('latitude')
            original_msg['params']['vehicle_status']['position_status'].pop('longitude')
            original_msg['params']['original_length'] = str(int(original_msg['params']['original_length'])-18)
            assert_equal(msg, original_msg)

        # 校验mysql
        tables = ['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs']
        checker.check_mysql_tables(charge_end_obj, tables)

        # 校验mongo 访问mongo需用欧洲堡垒机，欧洲堡垒机只能申请临时权限
        # collections = ['vehicle_position']
        # checker.check_mongodb_collections(charge_end_obj, collections, event_name='charge_end_event')