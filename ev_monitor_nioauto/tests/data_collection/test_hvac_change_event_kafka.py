#!/usr/bin/env python
# coding=utf-8

"""
:file: test_hvac_change_event_kafka.py
:author: chunming.liu
:Date: Created on 2019/1/8 下午5:04
:Description: 空调消息存储到kafka的swc-tsp-data_collection-test-vehicle_data供其他系统消费
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestHvacChangeMsg(object):
    def test_hvac_change_event_kafka(self, vid, publish_msg_by_kafka, cmdopt, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('hvac_change_event')

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))
