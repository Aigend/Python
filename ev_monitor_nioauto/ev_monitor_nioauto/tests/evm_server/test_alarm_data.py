#!/usr/bin/env python
# coding=utf-8

"""
@author: chunming.liu
@Date: 2019/1/17 <br/>
@Feature: 1)存在于vehicle_profile表、存在于vehicle_platform_config表的私人领域车，给国家平台和地方平台发送AlarmSignal中的EVM类alarm
          2）vehicle_platform_activated表中alarm_enable字段设成NULL或者1,会转发alarm给国家平台和地方平台
          3）vehicle_platform_activated表中alarm_enable字段设成其他值,不会转发alarm给国家平台和地方平台
          4）如果上报的消息中包含alarm_data（老协议），会优先使用这里面的EVM alarm数据发给国家平台和地方平台，而忽略AlarmSignal中的。

"""
import datetime
import time

import allure
import json
import pytest
from utils.commonlib import show_json
from utils.time_parse import time_sec_to_strtime


@pytest.mark.skip('manual')
class TestAlarm(object):
    def test_alarm_data_nation(self, env, mysql, publish_msg_by_kafka):
        # 上报
        vin = env['vehicles']['gb_public']['vin']
        vid = env['vehicles']['gb_public']['vehicle_id']

        alarm_data = {'common_failure': [{'alarm_tag': 2, 'alarm_level': 3}]}

        nextev_message, charge_update_obj = publish_msg_by_kafka('periodical_charge_update',
                                                                 vin=vin, vid=vid,
                                                                 sample_points=[{'alarm_data': alarm_data}])
        time.sleep(2)
        # 校验
        # sh_message_mock_server = mysql['rvs'].fetch('vehicle_data_mock',
        #                                             {"vin": vin,
        #                                              "sample_time": charge_update_obj['sample_points'][0]['sample_ts'] // 1000,
        #                                              "attribution": prepare[1]
        #                                              }
        #                                             )[0]
        sample_time = time_sec_to_strtime(charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        gb_message_mock_server = mysql['rvs'].fetch('vehicle_data_mock',
                                                    {"vin": vin,
                                                     "sample_time": sample_time,
                                                     "command": 2,
                                                     "attribution": 156})[0]

        # with allure.step("校验SH Mock Server收到了转发报警的数据"):
        #     allure.attach(show_json(sh_message_mock_server),"mock_server收到的内容")
        #     message_in_mock_server = json.loads(sh_message_mock_server['message'])
        #     assert message_in_mock_server['unique_id'] == vin
        #     assert message_in_mock_server['command'] == '2'  # 表示实时消息
        #     assert message_in_mock_server['ack'] == '254'
        #     assert message_in_mock_server['data_unit']['sample_ts'] == charge_update_obj['sample_points'][0]['sample_ts'] // 1000
        #     assert message_in_mock_server['data_unit']['sample_points']['alarm_data']['hi_alm_levl'] != 0
        #     assert message_in_mock_server['data_unit']['sample_points']['alarm_data']['common_alarm_flag'] != 0

        with allure.step("校验GB Mock Server收到了转发报警的数据"):
            allure.attach(show_json(gb_message_mock_server), "mock_server收到的内容")
            message_in_mock_server = json.loads(gb_message_mock_server['message'])
            assert message_in_mock_server['uniqueId'] == vin
            assert message_in_mock_server['commandId'] == 2  # 表示实时消息
            assert message_in_mock_server['ack'] == 254
            assert message_in_mock_server['dataUnit']['sampleTs'] == charge_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert message_in_mock_server['dataUnit']['reportInfoList'][4]['infoBody']['highestAlarmLevel'] != 0
            assert message_in_mock_server['dataUnit']['reportInfoList'][4]['infoBody']['commonAlarmFlag'] != 0
