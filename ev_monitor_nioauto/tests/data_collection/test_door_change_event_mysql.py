#!/usr/bin/env python
# coding=utf-8

"""
:file: test_door_change_event_mysql.py
:author: chunming.liu
:Date: Created on 2019/1/8 下午7:12
:Description: 车门状态变更事件存到Mysql的status_door表
"""
import pytest


class TestDoorStatusChangeMsg(object):
    @pytest.mark.parametrize('clear_fields', [['door_status.door_locks.account_id'], None], ids=['NT1', 'NT2'])
    def test_door_status_change_event_mysql(self, checker, publish_msg, clear_fields):
        # 构造并上报消息
        nextev_message, door_status_obj = publish_msg('door_change_event',
                                                      platform_type=1 if clear_fields is None else 0,
                                                      clear_fields=clear_fields)

        # 校验
        tables = ['status_door']
        checker.check_mysql_tables(door_status_obj, tables)

