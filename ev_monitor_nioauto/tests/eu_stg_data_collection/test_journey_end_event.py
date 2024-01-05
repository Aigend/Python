""" 
@author:dun.yuan
@time: 2021/6/20 12:53 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
import pytest
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestJourneyEndMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_journey_end_event(self, publish_msg, checker, vid, kafka, prepare):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, journey_end_obj = publish_msg('journey_end_event', sleep_time=30,
                                                      vehicle_status={"mileage": prepare['original_mileage'] + 1})

        # 校验cassandra
        tables ={'vehicle_data':['vehicle_id',
                                 'soc_status',
                                 'position_status',
                                 'vehicle_status',
                                 'process_id as journey_id',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(journey_end_obj, tables, event_name='journey_end_event')

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == journey_end_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))

        # 校验mysql
        tables =['status_position','status_vehicle', 'status_soc']
        checker.check_mysql_tables(journey_end_obj, tables)