#!/usr/bin/env python
# coding=utf-8


class TestHeatingStatusChangeMsg(object):
    def test_heating_status_change_event_mysql(self, checker, publish_msg):
        # 构造并上报消息
        nextev_message, heating_change_obj = publish_msg('heating_status_change_event')

        # 校验
        tables = ['status_heating']
        checker.check_mysql_tables(heating_change_obj, tables)
