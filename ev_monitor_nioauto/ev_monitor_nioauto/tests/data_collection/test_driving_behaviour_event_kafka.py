#!/usr/bin/env python
# coding=utf-8

"""
:file: test_driving_behaviour_event_kafka_mysql.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12 下午7:17
:Description: 驾驶行为事件上报，包含驾驶行为数据。
"""
import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestDrivingBehaviourMsg(object):
    def test_driving_behaviour_event(self, vid, kafka, cmdopt, publish_msg_by_kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('driving_behaviour_event')

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))