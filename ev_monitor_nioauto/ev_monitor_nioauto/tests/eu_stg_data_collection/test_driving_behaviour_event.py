""" 
@author:dun.yuan
@time: 2021/6/20 12:12 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestDrivingBehaviourMsg(object):
    def test_driving_behaviour_event(self, publish_msg, checker, kafka, vid):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, driving_behaviour_obj = publish_msg('driving_behaviour_event')

        # 校验cassandra
        tables = {'vehicle_data': ['vehicle_id',
                                   'driving_behaviour',
                                   'sample_ts']
                  }
        checker.check_cassandra_tables(driving_behaviour_obj, tables, event_name='driving_behaviour_event')

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == driving_behaviour_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))

        # mysql status_driving_behv表已停止更新
