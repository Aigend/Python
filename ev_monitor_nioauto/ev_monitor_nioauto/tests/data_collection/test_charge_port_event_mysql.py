#!/usr/bin/env python
# coding=utf-8

"""
:file: test_charge_port_event_mysql.py
:author: chunming.liu
:Date: Created on 2019/1/8 下午7:12
:Description: 充电口事件存储到Mysql的status_door中。
"""
import pytest


class TestChargePortChangeMsg(object):
    @pytest.mark.parametrize('clear_fields', [['door_status.door_locks.account_id'], None], ids=['NT1', 'NT2'])
    def test_charge_port_event_mysql(self, publish_msg, checker, clear_fields):
        # 构造并上报消息
        nextev_message, charge_port_obj = publish_msg('charge_port_event',
                                                      platform_type=1 if clear_fields is None else 0,
                                                      clear_fields=clear_fields)

        # 校验
        tables = ['status_door']
        checker.check_mysql_tables(charge_port_obj, tables)



