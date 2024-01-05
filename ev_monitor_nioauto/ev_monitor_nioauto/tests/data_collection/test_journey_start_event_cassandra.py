#!/usr/bin/env python
# coding=utf-8

"""
:file: test_journey_start_event_cassandra.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12
:Description: 行驶结束消息，包含position数据和soc数据
"""
import allure
from utils.time_parse import utc_to_local


class TestJourneyStartMsg(object):
    def test_journey_start_event(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, journey_start_obj = publish_msg('journey_start_event')

        # 校验
        tables = {
            'vehicle_data': ['vehicle_id',
                             'soc_status',
                             'position_status',
                             'vehicle_status',
                             'hvac_status',
                             'btry_pak_info',
                             'icc_id',
                             'process_id as journey_id',
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
        checker.check_cassandra_tables(journey_start_obj, tables, event_name='journey_start_event')

    def test_journey_start_event_v18(self, vid, publish_msg, checker, cassandra):
        # 构造并上报消息,proto版本大于18，journey start不再保存入driving data,由trip start替代
        nextev_message, journey_start_obj = publish_msg('journey_start_event', protobuf_v=18, sleep_time=5)

        # 校验
        tables = {
            'vehicle_data': ['vehicle_id',
                             'soc_status',
                             'position_status',
                             'vehicle_status',
                             'hvac_status',
                             'btry_pak_info',
                             'icc_id',
                             'process_id as journey_id',
                             'sample_ts']
        }
        checker.check_cassandra_tables(journey_start_obj, tables, event_name='journey_start_event')

        with allure.step("校验journey_start_event不再存入Cassandra的driving_data"):
            sample_ts = journey_start_obj['sample_ts']
            sample_date = utc_to_local(timestamp=sample_ts / 1000.0, offset_hour=8)
            event_in_cassandra = cassandra['datacollection'].fetch('driving_data',
                                                                   where_model={'vehicle_id': vid,
                                                                                'sample_ts': sample_ts,
                                                                                'sample_date': sample_date})
            assert len(event_in_cassandra) == 0
