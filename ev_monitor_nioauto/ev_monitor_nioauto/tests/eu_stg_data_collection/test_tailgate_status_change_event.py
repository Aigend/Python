""" 
@author:dun.yuan
@time: 2021/6/20 5:13 下午
@contact: dun.yuan@nio.com
@description: 后备箱状态变更事件存储到Cassandra的vehicle_data的door_status字段
@showdoc：
"""
import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestTailgateChangeMsg(object):
    def test_tailgate_status_change_event(self, publish_msg, checker, vid, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, tailgate_status_change_event_obj = publish_msg('tailgate_status_change_event', sleep_time=30)

        # 校验cassandra
        tables ={'vehicle_data':['vehicle_id',
                                 'door_status',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(tailgate_status_change_event_obj, tables, event_name='tailgate_status_change_event')

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == tailgate_status_change_event_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))

        # 校验mysql
        tables = ['status_door']
        checker.check_mysql_tables(tailgate_status_change_event_obj, tables)