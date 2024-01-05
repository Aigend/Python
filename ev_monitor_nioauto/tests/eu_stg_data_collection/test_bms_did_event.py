""" 
@author:dun.yuan
@time: 2021/6/18 1:33 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestBMSDidMsg(object):
    def test_bms_dids_event(self, publish_msg, checker, kafka, vid):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, bms_dids_event_obj = publish_msg('bms_did_event')

        # 校验cassandra
        tables = {'vehicle_data': ['vehicle_id',
                                   'bms_did_info',
                                   'sample_ts']}

        checker.check_cassandra_tables(bms_dids_event_obj, tables, event_name='bms_did_event')

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=30):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == bms_dids_event_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))