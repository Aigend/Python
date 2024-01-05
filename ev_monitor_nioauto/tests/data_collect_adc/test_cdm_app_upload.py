""" 
@author:dun.yuan
@time: 2022/1/27 10:50 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
import json
from utils.assertions import assert_equal


class TestCdmAppUpload(object):
    def test_cdm_app_upload(self, vid, publish_msg_by_kafka_adas, kafka, checker):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['adas_map'])

        with allure.step('上报report_cdm_version事件'):
            nextev_message, obj = publish_msg_by_kafka_adas('cdm_app_upload', event_type='report_cdm_version', platform_type=1)

        with allure.step('验证成功转发'):
            kafka_msg = None
            for data in kafka['comn'].consume(kafka['topics']['adas_map'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['type'] == 'report_cdm_version':
                    break
            assert_equal(json.loads(kafka_msg['payload']), obj['CdmAppUpload'])

        with allure.step('上报report_cdm_exception事件'):
            nextev_message, obj = publish_msg_by_kafka_adas('cdm_app_upload', event_type='report_cdm_exception', platform_type=1)

        with allure.step('验证成功转发'):
            kafka_msg = None
            for data in kafka['comn'].consume(kafka['topics']['adas_map'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['type'] == 'report_cdm_exception':
                    break
            assert_equal(json.loads(kafka_msg['payload']), obj['CdmAppUpload'])