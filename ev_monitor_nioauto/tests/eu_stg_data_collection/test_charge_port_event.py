""" 
@author:dun.yuan
@time: 2021/6/15 12:55 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestChargePortChangeMsg(object):
    def test_charge_port_event(self, publish_msg, checker, kafka, vid):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, charge_port_obj = publish_msg('charge_port_event', sleep_time=30)

        # 校验cassandra
        tables = {'vehicle_data': ['vehicle_id',
                                   'door_status',
                                   'sample_ts']
                  }
        checker.check_cassandra_tables(charge_port_obj, tables, event_name='charge_port_event')

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == charge_port_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))

        # 校验mysql
        tables = ['status_door']
        checker.check_mysql_tables(charge_port_obj, tables)