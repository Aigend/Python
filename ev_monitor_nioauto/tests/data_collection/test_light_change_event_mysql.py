#!/usr/bin/env python
# coding=utf-8

"""
:file: test_light_change_event_mysql.py
:author: chunming.liu
:Date: Created on 2019/1/12
:Description: 电灯变化事件存储到Mysql的status_light表
"""
import allure
import time

from utils import message_formator
from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime


class TestLightChangeMsg(object):
    def test_light_change_event_mysql(self, checker, publish_msg):
        # 构造并上报消息
        nextev_message, light_change_obj = publish_msg('light_change_event')

        # 校验
        tables = ['status_light']
        checker.check_mysql_tables(light_change_obj, tables)

    def test_publish_ts_less_than_sample_ts(self, vid, checker, publish_msg):
        # TODO 和帅君确认一下这个校验是每个event单独还是统一校验
        with allure.step("校验 publish_ts和sample_ts中取最小一个值做mysql中的sample_time"):
            # 构造并上报消息
            sample_ts = int(round(time.time() * 1000))
            publish_ts = sample_ts - 2000
            nextev_message, obj = publish_msg('light_change_event', sample_ts=sample_ts, publish_ts=publish_ts)

            light_status_in_mysql =checker.mysql.fetch('status_light', {"id": vid, 'sample_time': timestamp_to_utc_strtime(publish_ts)}, exclude_fields=['update_time'])[0]

            # 校验mysql状态表的sample_time取自更小的publish_ts时间
            assert_equal(light_status_in_mysql['sample_time'], timestamp_to_utc_strtime(publish_ts))

            # 校验其他数据正常存储到状态表中
            formator = message_formator.MessageFormator(vid)
            light_status_in_message = formator.to_mysql_status_light(obj['light_status'])
            light_status_in_mysql.pop('sample_time')
            light_status_in_message.pop('sample_time')
            assert_equal(light_status_in_mysql, light_status_in_message)


