""" 
@author:dun.yuan
@time: 2021/12/31 3:34 下午
@contact: dun.yuan@nio.com
@description:
@showdoc：
"""
import allure
import json
from utils.assertions import assert_equal


class TestMapUpdateTile(object):
    def test_map_update_tile(self, vid, publish_msg_by_kafka_adas, kafka, checker):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['adas_map'])

        with allure.step('上报自动泊车失败事件'):
            nextev_message, obj = publish_msg_by_kafka_adas('map_update_tile', platform_type=1)

        with allure.step('验证成功转发自动泊车事件'):
            kafka_msg = None
            for data in kafka['comn'].consume(kafka['topics']['adas_map'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['type'] == 'map_update_tile':
                    break
            assert_equal(json.loads(kafka_msg['payload']), obj['map_update_tile'])
