#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:kangkai.cao
@time: 2021/11/03
@api: GET_/api/XXX 【必填】
@showdoc: XXX
@description: 脚本描述
"""

import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime


class TestTripEndMsg(object):
    def test_trip_end_event(self, vid, checker, publish_msg, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        with allure.step("上报事件trip_end_event"):
            nextev_message, trip_end_obj = publish_msg('trip_end_event')

        with allure.step("检验cassandra trip_status表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'trip_status',
                                       'position_status',
                                       'soc_status',
                                       'vehicle_status',
                                       'sample_ts']
                      }
            checker.check_cassandra_tables(trip_end_obj, tables, event_name='trip_end_event')

        with allure.step("检验向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == trip_end_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break
        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            parse_msg = parse_nextev_message(nextev_message)
            parse_msg["params"]["vehicle_status"]["position_status"].pop("latitude")
            parse_msg["params"]["vehicle_status"]["position_status"].pop("longitude")
            parse_msg["params"].pop("original_length")
            msg["params"].pop("original_length")
            assert_equal(msg, parse_msg)

        with allure.step("检验mysql status_trip表更新"):
            tables = ['status_trip']
            for table in tables:
                assert len(checker.mysql.fetch(table, {'id': vid, 'sample_time': timestamp_to_utc_strtime(trip_end_obj['sample_ts'])},
                                               fields=['id'])) == 1