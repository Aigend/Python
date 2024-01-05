#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:kangkai.cao
@time: 2021/11/03
@api: GET_/api/XXX 【必填】
@showdoc: XXX
@description: 充电开始事件，包含电池数据
"""

import pytest
from nio_messages.nextev_msg import parse_nextev_message
from utils.time_parse import timestamp_to_utc_strtime


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
        }
        checker.check_cassandra_tables(charge_start_obj, tables, event_name='charge_start_event')

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == charge_start_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        # 校验mysql
        tables = ['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs']
        for table in tables:
            assert len(checker.mysql.fetch(table, {'id': vid, 'sample_time': timestamp_to_utc_strtime(charge_start_obj['sample_ts'])},
                                           fields=['id'])) == 1