""" 
@author:dun.yuan
@time: 2021/6/20 5:48 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestVehicleEnergyMsg(object):
    def test_vehicle_energy_event_kafka(self, vid, kafka, publish_msg, checker):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, obj = publish_msg('vehicle_energy_event')

        # 校验cassandra
        tables = {'vehicle_data': ['vehicle_id',
                                   'vehicle_energy_status',
                                   'sample_ts']}

        checker.check_cassandra_tables(obj, tables, event_name='vehicle_energy_event')

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))