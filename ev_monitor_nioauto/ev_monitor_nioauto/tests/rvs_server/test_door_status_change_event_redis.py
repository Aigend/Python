#!/usr/bin/env python
# coding=utf-8

"""
:file: test_door_change_event_cassandra.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12 下午7:12
:Description: 车门状态变更事件存到Cassandra的vehicle_data和vehicle_history的door_status字段
"""

import allure


class TestDoorStatusChangeMsg(object):
    def test_door_status_change_event_redis(self, vid, checker, publish_msg, cmdopt):
        # 清除redis 缓存
        # cmdopt = 'staging' if cmdopt == 'stg' else cmdopt
        # with allure.step("清除redis 缓存"):
            # checker.redis.delete(
            #     'remote_vehicle_{cmdopt}:vehicle_status:{vid}:DoorStatus'.format(cmdopt=cmdopt, vid=vid))

        # 构造并上报消息
        nextev_message, door_change_obj = publish_msg('door_change_event')

        # 校验
        keys = ['DoorStatus']
        checker.check_redis(door_change_obj, keys, event_name='door_change_event',clear_none=True,
                            sample_ts=door_change_obj['sample_ts'])
