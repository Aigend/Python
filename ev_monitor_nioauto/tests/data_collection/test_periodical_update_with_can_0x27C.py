""" 
@author:dun.yuan
@time: 2022/5/7 12:21 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：https://jira.nioint.com/browse/CVS-16651
"""
import pytest
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestReportCan0x27C(object):
    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update'])
    def test_report_can_0x27c(self, event_name, vid, checker, publish_msg, kafka, env):
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])
        with allure.step("上报周期事件"):
            nextev_message, obj = publish_msg(event_name, sample_points=[{'can_msg': {
                'can_data': [{
                        'msg_id': 590,
                        'value': 'ffffffffffffffff'
                    }],
                'can_news': [{'msg_id': 0x27C,
                              'value': ['8888888888888888', '0000000000000000', 'ffffffffffffffff']}]
            }}])

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == obj['sample_points'][0]['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            msg.pop('params') if msg else None
            nextev_obj = parse_nextev_message(nextev_message)
            nextev_obj.pop('params')
            assert_equal(msg, nextev_obj)

        with allure.step("检查cassandra vehicle_data表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'charging_info',
                                       'soc_status',
                                       'body_status',
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
                                       'sample_ts']
                      }
            if event_name == 'periodical_journey_update':
                tables['vehicle_data'].append('trip_status')
                tables['vehicle_data'].remove('charging_info')
            checker.check_cassandra_tables(obj['sample_points'][0], tables,
                                           event_name=event_name,
                                           sample_ts=obj['sample_points'][0]['sample_ts'])
