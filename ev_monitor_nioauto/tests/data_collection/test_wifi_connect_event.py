""" 
@author:dun.yuan
@time: 2022/6/9 8:46 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestWifiConnect(object):
    def test_wifi_connect_event(self, vid, checker, publish_msg_by_kafka, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        with allure.step("上报事件wifi_connect_msg"):
            nextev_message, wifi_connect_obj = publish_msg_by_kafka('wifi_connect_event', protobuf_v=18, platform_type=2)

        with allure.step("检验向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == wifi_connect_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break
        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            assert_equal(msg, expect)

        with allure.step("检验cassandra wifi_connect表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'wifi_connect_status',
                                       'sample_ts']}
            checker.check_cassandra_tables(wifi_connect_obj, tables, event_name='wifi_connect_event')
