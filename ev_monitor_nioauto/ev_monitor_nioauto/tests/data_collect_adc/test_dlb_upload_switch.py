""" 
@author:dun.yuan
@time: 2022/3/28 10:51 AM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
import json
from utils.assertions import assert_equal


class TestDlbUploadSwitch(object):
    def test_dlb_upload_switch(self, vid, publish_msg_by_kafka_adas, kafka, checker):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['adas_map'])

        with allure.step('上报dlb_upload_switch事件'):
            nextev_message, obj = publish_msg_by_kafka_adas('dlb_upload_switch', platform_type=1)

        with allure.step('验证成功转发'):
            kafka_msg = None
            for data in kafka['comn'].consume(kafka['topics']['adas_map'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['type'] == 'dlb_upload_switch':
                    break
            assert_equal(json.loads(kafka_msg['payload']), obj['dlb_upload_switch'])
