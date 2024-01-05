""" 
@author:dun.yuan
@time: 2021/6/20 5:40 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestWindowChangeMsg(object):
    def test_window_change_event(self, publish_msg, checker, vid, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, window_change_event_obj = publish_msg('window_change_event', sleep_time=30)

        # 校验cassandra
        tables ={'vehicle_data':['vehicle_id',
                                 'window_status',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(window_change_event_obj, tables, event_name='window_change_event')

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == window_change_event_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))

        # 校验
        tables = ['status_window']
        checker.check_mysql_tables(window_change_event_obj, tables)