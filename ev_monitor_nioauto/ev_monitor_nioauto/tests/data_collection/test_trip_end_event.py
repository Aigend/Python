""" 
@author:dun.yuan
@time: 2021/3/23 8:36 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestTripEndMsg(object):
    def test_trip_end_event(self, vid, checker, publish_msg, kafka, cmdopt):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        with allure.step("上报事件trip_end_event"):
            nextev_message, trip_end_obj = publish_msg('trip_end_event', protobuf_v=18)

        with allure.step("检验cassandra trip_status表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'trip_status',
                                       'position_status',
                                       'soc_status',
                                       'vehicle_status',
                                       'sample_ts'],
                      'driving_data': ['dump_enrgy',
                                       'mileage',
                                       'position',
                                       'posng_valid_type',
                                       'soc',
                                       'speed',
                                       'trip_odometer',
                                       'realtime_power_consumption',
                                       'process_id',
                                       'sample_ts']
                      }
            checker.check_cassandra_tables(trip_end_obj, tables, event_name='trip_end_event')

        with allure.step("检验向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == trip_end_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break
        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            if 'marcopolo' in cmdopt:
                msg['params'].pop('original_length')
                expect['params'].pop('original_length')
                expect['params']['vehicle_status']['position_status'].pop('latitude')
                expect['params']['vehicle_status']['position_status'].pop('longitude')
            assert_equal(msg, expect)
