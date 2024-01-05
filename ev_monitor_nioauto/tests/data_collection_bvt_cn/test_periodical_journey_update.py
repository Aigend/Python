""" 
@author:dun.yuan
@time: 2021/6/20 4:46 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import datetime

import pytest
import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestJourneyjourneyMsg(object):
    @pytest.fixture(scope='function', autouse=True)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    @pytest.mark.parametrize("reissue", [True, False], ids=['reissue is True', 'reissue if False'])
    def test_periodical_journey(self, publish_msg, reissue, checker, vid, kafka, prepare):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, charge_journey_obj = publish_msg('periodical_journey_update',
                                                         reissue=reissue,
                                                         sample_points=
                                                         [{
                                                          "vehicle_status": {"mileage": prepare['original_mileage'] + 1}
                                                         }])

        # 校验
        # 周期上报事件的alarm_signal存到cassandra里的alarm_data，alarm_data存到cassandra里的re_alarm_data里，
        tables = {'vehicle_data': ['vehicle_id',
                                   'soc_status',
                                   'body_status',
                                   'trip_status',
                                   'position_status',
                                   'vehicle_status',
                                   'bms_status',
                                   'driving_data',
                                   'driving_motor_status',
                                   'extremum_data',
                                   'occupant_status',
                                   'hvac_status',
                                   'tyre_status',
                                   'can_msg',
                                   'can_signal',
                                   're_alarm_data',
                                   'alarm_data',
                                   'evm_flag',
                                   'sample_ts'],
                  'driving_data': ['dump_enrgy',
                                   'mileage',
                                   'position',
                                   'posng_valid_type',
                                   'soc',
                                   'speed',
                                   'realtime_power_consumption',
                                   'sample_ts']
                  }
        checker.check_cassandra_tables(charge_journey_obj['sample_points'][0], tables,
                                       event_name='periodical_journey_update',
                                       sample_ts=charge_journey_obj['sample_points'][0]['sample_ts'])

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=30):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == charge_journey_obj['sample_points'][0]['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            msg.pop('params') if msg else None
            nextev_obj = parse_nextev_message(nextev_message)
            nextev_obj.pop('params')
            assert_equal(msg, nextev_obj)

        # 校验
        tables = ['status_position', 'status_vehicle', 'status_soc',
                  'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                  'status_extremum_data', 'status_driving_data', 'status_hvac',
                  'status_tyre']
        for sample_point in charge_journey_obj['sample_points']:
            checker.check_mysql_tables(sample_point, tables)