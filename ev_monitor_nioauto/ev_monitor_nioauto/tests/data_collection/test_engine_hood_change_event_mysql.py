#!/usr/bin/env python
# coding=utf-8

"""
:file: test_engine_hood_status_change_event_mysql.py
:author: chunming.liu
:Date: Created on 2019/1/12 下午7:12
:Description: 发动机罩变更事件存储到Mysql的status_door中
"""


class TestEngineHoodChangeMsg(object):
    def test_engine_hood_status_change_event(self, checker, publish_msg):
        # 构造并上报消息
        nextev_message, engine_hood_status_change_obj = publish_msg('engine_hood_status_change_event')

        # 校验
        tables = ['status_door']
        checker.check_mysql_tables(engine_hood_status_change_obj, tables)
