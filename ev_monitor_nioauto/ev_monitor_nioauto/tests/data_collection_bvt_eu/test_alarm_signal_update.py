#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:kangkai.cao
@time: 2021/11/02
@api: GET_/api/XXX 【必填】
@showdoc: XXX
@description: 脚本描述
"""

import allure
from utils.assertions import assert_equal


class TestAlarmSignalUpdateMSG(object):
    def test_alarm_signal_update(self, publish_msg, checker):
        with allure.step("校验 alarm_signal_update 事件不更新所有状态表"):
            nextev_message, alarm_signal_update = publish_msg('alarm_signal_update_event')

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
        # 需上线这俩个字段，现在会失败
        # alarm_signal_update['sample_points']['driving_data'].pop('veh_dispd_spd')
        # alarm_signal_update['sample_points']['driving_data'].pop('veh_outd_hum')
        checker.check_cassandra_tables(alarm_signal_update['sample_points'], tables,
                                       event_name='alarm_signal_update_event',
                                       sample_ts=alarm_signal_update['sample_ts'])