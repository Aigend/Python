#!/usr/bin/env python
# coding=utf-8

"""
:file: test_journey_start_event_kafka.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12
:Description: 行驶结束消息，包含position数据和soc数据
"""

import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestJourneyStartMsg(object):
    def test_journey_start_event(self, vid, cmdopt, kafka, publish_msg_by_kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('journey_start_event')

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        #新增bid字段，验证推送到大数据平台的消息里携带
        assert 'bid' in msg['params']['vehicle_status']['battery_package_info']['btry_pak_encoding'][0]
        msg['params']['vehicle_status']['battery_package_info']['btry_pak_encoding'][0].pop('bid')
        msg['params']['original_length'] = str(int(msg['params']['original_length'])-34)

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            if 'marcopolo' in cmdopt:
                msg['params'].pop('original_length')
                expect['params'].pop('original_length')
                expect['params']['vehicle_status']['position_status'].pop('latitude')
                expect['params']['vehicle_status']['position_status'].pop('longitude')
                expect['params']['vehicle_status']['battery_package_info']['btry_pak_encoding'][0].pop('re_encoding')
                expect['params']['vehicle_status']['battery_package_info']['btry_pak_encoding'][0]['nio_encoding'] = \
                    expect['params']['vehicle_status']['battery_package_info']['btry_pak_encoding'][0]['nio_encoding'][:27]
            assert_equal(msg, expect)

