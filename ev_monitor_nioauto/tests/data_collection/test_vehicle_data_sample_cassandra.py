#!/usr/bin/env python
# coding=utf-8

"""
:author: li.liu
:Date: Created on 2019/1/29 下午2:01
:Description: 上报周期性充电消息，校验消息根据采样频率存储在cassandra的vehicle_data_sample表中。
"""

import time
import allure
import datetime
import pytest

from nio_messages import periodical_charge_update
from utils.assertions import assert_equal


INTERVAL = 300  #Sample inteval set 300 second
RAW_UPDATE_INTERVAL = 5 # Raw message update interval will be 5s

@pytest.mark.skip('skip')
class TestVehicle_data_sample(object):
    def test_vehicle_data_sample(self, env, cassandra, tsp_agent_for_sample):
        # 构造并上报消息
        first_sample_ts = int(round(time.time() * 1000))
        vin = env['vehicles']['vehicle_for_sample']['vin']
        vid = env['vehicles']['vehicle_for_sample']['vehicle_id']
        need_sampled = []
        need_sampled_ts = []

        tmp = []
        with allure.step("上报charge_update_message"):
            # 上报数据，设为每隔5秒一个，共报121个
            for i in range(121):
                sample_ts = first_sample_ts + i*1000*5
                tmp.append(sample_ts)
                nextev_message, charge_update_obj = periodical_charge_update.generate_message(vin,
                                                                                              sample_points=[{
                                                                                                  'sample_ts': sample_ts

                                                                                              }])

                tsp_agent_for_sample.publish(bytearray(nextev_message))
                time.sleep(0.5)
                if self._need_sampled(sample_ts):
                    sample_ts_format = datetime.datetime.utcfromtimestamp(sample_ts / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + 'Z'

                    need_sampled.append(charge_update_obj['sample_points'][0])
                    need_sampled_ts.append(sample_ts_format)

        # Revert the need_sampled to make it ordered by sample_ts desc
        need_sampled.reverse()
        time.sleep(2)

        # 校验 cassandra vehicle_data_sample 表
        with allure.step("校验Cassandra的vehicle_data_sample表有两条记录"):

            sample_date = datetime.datetime.fromtimestamp(first_sample_ts / 1000.0).strftime('%Y-%m')

            sampling_data_in_cassandra = cassandra['datacollection'].fetch('vehicle_data_sample',
                                                                           where_model={'vehicle_id': vid,
                                                                            'sample_date': str(sample_date),
                                                                            'sample_interval':str(INTERVAL),
                                                                            'sample_ts in': need_sampled_ts,
                                                                            'msg_type': 'periodical_charge_update'
                                                                            },
                                                                           fields=['sample_date',
                                                                            'sample_interval',
                                                                            'soc',
                                                                            'sample_ts']
                                                                           )

            sampling_data_in_msg = []
            for item in need_sampled:
                data = {}
                data['sample_date'] = datetime.datetime.fromtimestamp(item['sample_ts'] / 1000.0).strftime('%Y-%m')
                data['sample_interval'] = str(INTERVAL)
                data['sample_ts'] = datetime.datetime.utcfromtimestamp(item['sample_ts']/1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]+'Z'
                data['soc'] = str(item['soc_status']['soc'])
                sampling_data_in_msg.append(data)

            assert_equal(len(sampling_data_in_cassandra), 2)
            assert_equal(sampling_data_in_cassandra, sampling_data_in_msg)


    def _need_sampled(self, sample_ts):
        remainder = (sample_ts/1000)%INTERVAL
        if(INTERVAL - remainder <= RAW_UPDATE_INTERVAL):
            return True
        return False

