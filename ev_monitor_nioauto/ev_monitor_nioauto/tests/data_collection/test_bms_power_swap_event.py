""" 
@author:dun.yuan
@time: 2021/6/30 1:02 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestBMSPowerSwapMsg(object):
    def test_bms_power_swap_event(self, vid, publish_msg, checker, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, bms_power_swap_event_obj = publish_msg('bms_power_swap_event')

        # 校验cassandra
        tables = {'vehicle_data': ['bms_did_info']}

        checker.check_cassandra_tables(bms_power_swap_event_obj, tables, event_name='bms_power_swap_event')

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=30):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == bms_power_swap_event_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))