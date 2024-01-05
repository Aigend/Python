""" 
@author:dun.yuan
@time: 2021/12/30 5:47 下午
@contact: dun.yuan@nio.com
@description: 换电站自动泊车失败推送事件给PE
@showdoc：
"""
import allure
import time
import json
from utils.assertions import assert_equal


class TestAdcForwardParkFail(object):
    def test_forward_auto_park_fail(self, vid, publish_msg_by_kafka_adas, kafka, checker):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['adas_fail'])

        with allure.step('上报自动泊车失败事件'):
            time.sleep(5)
            nextev_message, obj = publish_msg_by_kafka_adas('tsp_log',
                                                            tsp_log_list=[{'key': 'FeatureEvent',
                                                                           'comment': 'FE_PSAP_HMI_Status_mp',
                                                                           'value': 6}])

        with allure.step('验证成功转发自动泊车事件'):
            expect = {"sample_time": obj["AdasHeader"]["timestamp"],
                      "fail_code": 10,
                      "vehicle_id": vid,
                      "fail_msg": "psap_abort"}
            kafka_msg = None
            for data in kafka['comn'].consume(kafka['topics']['adas_fail'], timeout=60):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['sample_time'] == expect['sample_time']:
                    break
            assert_equal(kafka_msg, expect)
