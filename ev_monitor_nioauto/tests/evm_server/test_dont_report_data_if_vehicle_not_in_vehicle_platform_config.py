#!/usr/bin/env python
# coding=utf-8

"""
@author: chunming.liu
@Date: 2019/1/17 <br/>
@Feature: 1)存在于vehicle_profile表、但不存在于vehicle_platform_config表的车，不存入cassandra和转发给政府平台
"""
import datetime
import random

import allure
import pytest

from nio_messages import wti
from utils.assertions import assert_equal
from utils.time_parse import time_sec_to_strtime


@pytest.mark.test
class TestVehicleNotInVehiclePlatformConfig(object):
    def test_dont_report_data_to_gb(self, env, cmdopt, mysql, kafka, cassandra, publish_msg_by_kafka):
        # 上报
        vin = env['vehicles']['in_vehicle_profile_not_in_vehicle_platform_config']['vin']
        vid = env['vehicles']['in_vehicle_profile_not_in_vehicle_platform_config']['vehicle_id']

        alarm_singal_list = random.sample(wti.EVM_WTI_SIGNAL, 4)
        nextev_message, charge_update_obj = publish_msg_by_kafka(event_name='periodical_charge_update',
                                                   vin=vin, vid=vid,
                                                   sample_points=[{
                                                       'alarm_signal':
                                                           {'signal_int': alarm_singal_list},

                                                   }]
                                                   )

        # 校验
        insert_date = datetime.datetime.fromtimestamp(
            charge_update_obj['sample_points'][0]['sample_ts'] // 1000).strftime('%Y-%m-%d-%H')
        evm_message_in_cassandra = cassandra['datacollection'].fetch('evm_message',
                                                                     {'vin': vin,
                                                                      'insert_date': insert_date
                                                                      },
                                                                     [
                                                                         "blobAsBigint(timestampAsBlob(sample_ts)) as sample_ts"
                                                                     ]
                                                                     )
        sample_time = time_sec_to_strtime(charge_update_obj['sample_points'][0]['sample_ts'] // 1000)
        message_mock_server = mysql['rvs'].fetch('vehicle_data_mock',
                                                 {"vin": vin,
                                                  "sample_time": sample_time
                                                  }
                                                 )

        with allure.step("数据不会存入Cassandra数据库的evm_message表中"):
            assert_equal(bool(evm_message_in_cassandra), False)

        with allure.step("数据不会转发给Mock Server"):
            assert_equal(bool(message_mock_server), False)
