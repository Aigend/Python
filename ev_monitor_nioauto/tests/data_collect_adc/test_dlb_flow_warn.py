""" 
@author:dun.yuan
@time: 2022/3/2 3:22 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
import json
from utils.assertions import assert_equal


class TestDlbFlowWarn(object):
    def test_dlb_flow_warn(self, vid, publish_msg_by_kafka_adas, kafka, checker):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['adas_map'])

        with allure.step('上报dlb流量信息'):
            nextev_message, obj = publish_msg_by_kafka_adas('dlb_flow_warn', platform_type=1,
                                                            dlb_flow_warn_data={'upload_info': {
                                                                'event_info': [{'app_name': 'cdm_app',
                                                                                'event_name': 'cdm',
                                                                                'event_flow': 1000},
                                                                               {'app_name': 'log_manager_app',
                                                                                'event_name': 'log',
                                                                                'event_flow': 2000}]
                                                            }})

        with allure.step('验证成功转发'):
            kafka_msg = None
            for data in kafka['comn'].consume(kafka['topics']['adas_map'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['type'] == 'dlb_flow_warn':
                    break
            assert_equal(json.loads(kafka_msg['payload']), obj['dlb_flow_warn'])
