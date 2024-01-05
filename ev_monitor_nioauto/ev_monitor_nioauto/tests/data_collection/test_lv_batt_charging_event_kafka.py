#!/usr/bin/env python
# coding=utf-8

import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestLvBattChargingMsg(object):
    def test_lv_batt_charging_event_kafka(self, vid, kafka, publish_msg_by_kafka):
        """
        vehicle_data kafka 加上发送未解析的can msg
        未解析的 msg_id 为原 msg_id 取负数，value为hexstring，即表示十六进制的字符串
        """
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('lv_batt_charging_event')

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            msg.pop('params') if msg else None
            nextev_obj = parse_nextev_message(nextev_message)
            nextev_obj.pop('params')
            assert_equal(msg, nextev_obj)
