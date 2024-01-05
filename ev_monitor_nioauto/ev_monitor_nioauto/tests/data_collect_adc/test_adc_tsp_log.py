""" 
@author:dun.yuan
@time: 2022/3/11 8:25 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import random

import allure
import json
from utils.assertions import assert_equal


class TestAdcTspLog(object):
    def test_adc_tsp_log(self, vid, publish_msg_by_kafka_adas, kafka, checker):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['adas_map'])
        event_type = random.choice(['dlb_app_fault', 'fault_mgr', 'arg_app_fault', 'coredump_msg', 'function_fault'])
        with allure.step('上报tsp log'):
            nextev_message, obj = publish_msg_by_kafka_adas('tsp_log_nt2', platform_type=1, event_type=event_type)

        with allure.step('验证成功转发'):
            kafka_msg = None
            for data in kafka['comn'].consume(kafka['topics']['adas_map'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['type'] == event_type and kafka_msg['vehicle_id'] == vid:
                    break
            assert_equal(json.loads(kafka_msg['payload']), obj['TspLogList'])
