#!/usr/bin/env python
# coding=utf-8

import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestBMSDidMsg(object):
    def test_bms_did_event_kafka(self, vid, kafka, publish_msg_by_kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('bms_did_event')

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=30):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))
