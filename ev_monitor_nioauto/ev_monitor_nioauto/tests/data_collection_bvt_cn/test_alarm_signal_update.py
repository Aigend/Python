""" 
@author:dun.yuan
@time: 2021/6/19 12:21 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from utils.assertions import assert_equal


class TestAlarmSignalUpdateMSG(object):
    def test_alarm_signal_update(self, publish_msg, checker):
        with allure.step("校验 alarm_signal_update 事件不更新所有状态表"):
            tables = ['status_position', 'status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']

            data_mysql_old = checker.get_mysql_status_tables(tables)

            nextev_message, alarm_signal_update = publish_msg('alarm_signal_update_event',
                                                              signallib_version='BL00.07.00_DA_01')

            data_mysql_new = checker.get_mysql_status_tables(tables)

            assert_equal(data_mysql_old, data_mysql_new)

        # 校验
        # 注意alarm_signal会存到cassandra里的alarm_data
        tables = {'vehicle_data': ['vehicle_id',
                                   'soc_status',
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
                                   'alarm_data',
                                   'sample_ts']
                  }

        alarm_signal_update['sample_points']['alarm_signal'] = alarm_signal_update.pop('alarm_signal')
        checker.check_cassandra_tables(alarm_signal_update['sample_points'], tables,
                                       event_name='alarm_signal_update_event',
                                       sample_ts=alarm_signal_update['sample_ts'])
