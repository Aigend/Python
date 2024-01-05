#!/usr/bin/env python
# coding=utf-8

"""
@Feature: 当上报信息中有报警数据时，在上报国家，地方平台成功后，发送包含报警数据sampleTs的消息到KAFKA。Slytherin 会消费它更新history_wti_alarm表
"""
import json
import allure
import pytest

from utils.assertions import assert_equal


@pytest.mark.test
class TestChargeUpdateMsg(object):
    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_periodical_charge_update(self, event_name, kafka, vid, publish_msg_by_kafka):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['alarm_reported'])

        # 构造并上报消息
        nextev_message, charge_update_obj = publish_msg_by_kafka(event_name,
                                                                 sample_points=[{
                                                                     "alarm_signal": {
                                                                         "signal_int": [

                                                                             {"name": "PEUFMotorTempAlarm", "value": 2}

                                                                         ]}}],
                                                                 clear_fields=["sample_points[0].alarm_data"])
        kafka_msg = None
        is_found = False
        for data in kafka['cvs'].consume(kafka['topics']['alarm_reported'], timeout=10):
            kafka_msg = json.loads(str(data, encoding='utf-8'))
            if vid == kafka_msg['vehicle_id']:
                is_found = True
                break
        with allure.step('校验 {}'.format(kafka['topics']['alarm_reported'])):
            assert_equal(is_found, True)
            assert_equal(kafka_msg['plateform_type'], "NATIONAL")
