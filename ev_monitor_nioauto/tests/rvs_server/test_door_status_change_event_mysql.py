#!/usr/bin/env python
# coding=utf-8

"""
@author:hongzhen.bi
@time: 2020/06/17 17:01
@contact: hongzhen.bi@nio.com
@description: 处理包含车门状态的所有上报消息，将用户信息记录到vehicle_driving_event表
"""
import random

from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime

import allure
import pytest


class TestDoorStatusChangeMsg(object):
    @pytest.mark.skip(reason='rvs server不再通过上报门事件来存储用车人的id，cdc会调用tsp接口(http://showdoc.nevint.com/index.php?s=/11&page_id=1341)存储。'
                             '另外之前rvs server因操作表vehicle_driving_event会发生慢查询。')
    def test_door_status_change_event_mysql(self, vid, mysql, publish_msg, cmdopt):
        user_1 = random.randint(0, 9999)
        # 用户user1开车门
        nextev_message, door_change_obj_1st = publish_msg('door_change_event',
                                                          door_status={
                                                              "door_locks": {"user_id": user_1}
                                                          })
        trigger_time_1st = timestamp_to_utc_strtime(door_change_obj_1st['sample_ts'])
        mysql_data_1st_before = mysql['rvs'].fetch('vehicle_driving_event', {'account_id': user_1, 'vehicle_id': vid, 'start_time': trigger_time_1st})

        # 用户user1重复开车门
        nextev_message, door_change_obj_2st = publish_msg('door_change_event',
                                                          door_status={
                                                              "door_locks": {"user_id": user_1}
                                                          })
        trigger_time_2nd = timestamp_to_utc_strtime(door_change_obj_2st['sample_ts'])
        mysql_data_2nd = mysql['rvs'].fetch('vehicle_driving_event', {'account_id': user_1, 'vehicle_id': vid, 'start_time': trigger_time_2nd})

        with allure.step('校验用户重复触发车辆上报车门事件时，vehicle_driving_event不会记录用户登录信息'):
            assert_equal(bool(mysql_data_2nd), False)
            mysql_data_1st_after = mysql['rvs'].fetch('vehicle_driving_event', {'account_id': user_1, 'vehicle_id': vid, 'start_time': trigger_time_1st})
            assert_equal(mysql_data_1st_after, mysql_data_1st_before)

        # 用户user2开车门
        user_2 = user_1 + 1
        nextev_message, door_change_obj_3rd = publish_msg('door_change_event',
                                                          door_status={
                                                              "door_locks": {"user_id": user_2}
                                                          })
        trigger_time = timestamp_to_utc_strtime(door_change_obj_3rd['sample_ts'])
        mysql_data_3rd = mysql['rvs'].fetch('vehicle_driving_event', {'account_id': user_2, 'vehicle_id': vid, 'start_time': trigger_time})

        with allure.step('校验不同用户分别触发同一车辆上报车门事件时，vehicle_driving_event会分别记录用户登录信息，最近的start_time为上一次的end_time'):
            mysql_data_1st = mysql['rvs'].fetch('vehicle_driving_event', {'account_id': user_1, 'vehicle_id': vid, 'start_time': trigger_time_1st})
            assert_equal(mysql_data_1st[0]['end_time'], mysql_data_3rd[0]['start_time'])

        with allure.step('校验vehicle_driving_event的source_type和access_mode'):
            entry_meth = door_change_obj_3rd['door_status']['door_locks']['entry_meth']
            source_type = None if entry_meth == 7 else str(entry_meth)
            assert_equal(mysql_data_3rd[0]['source_type'], source_type)
            assert_equal(mysql_data_3rd[0]['access_mode'], door_change_obj_3rd['door_status']['door_locks']['access_mode'])
