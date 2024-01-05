#!/usr/bin/env python
# coding=utf-8

"""
:author: li.liu
:Description: 信号报警，包含国标报警和自定义报警的校验
"""


class TestAlarmSignalUpdateMSG(object):
    def test_alarm_signal_update(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, alarm_signal_update = publish_msg('alarm_signal_update_event',
                                                          signallib_version='BL00.07.00_DA_01')

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
                                   'alarm_data',
                                   'can_signal',
                                   'sample_ts']
                  }

        alarm_signal_update['sample_points']['alarm_signal'] = alarm_signal_update.pop('alarm_signal')
        checker.check_cassandra_tables(alarm_signal_update['sample_points'], tables,
                                       event_name='alarm_signal_update_event',
                                       sample_ts=alarm_signal_update['sample_ts']
                                       )

