#!/usr/bin/env python
# coding=utf-8

"""
:file: test_window_change_event_mysql.py
:author: chunming.liu
:Date: Created on 2019/1/12 下午7:57
:Description: 车窗事件消息存储到Mysql.status_window
"""
import random
import allure
import pytest

from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime


class TestWindowChangeMsg(object):
    def test_window_change_event_mysql(self, checker, publish_msg):
        # 上报
        nextev_message, window_change_event_obj = publish_msg('window_change_event')

        # 校验
        tables = ['status_window']
        checker.check_mysql_tables(window_change_event_obj, tables)

    def test_invaid_posn(self, vid, checker, publish_msg):
        with allure.step("校验车窗位置数据必须介于0-100之间。例外：window相关posn可以等于127，sun_roof_posn可为101，102，127"):
            # 原始
            window_status_in_mysql_old = checker.mysql.fetch('status_window', {"id": vid}, exclude_fields=['update_time', 'sun_roof_posn_sts', 'sample_time'])[0]

            # 上报
            window_status = {
                'window_positions':{
                    'win_frnt_le_posn':111,
                    'win_frnt_ri_posn':101,
                    'win_re_le_posn':-1,
                    'win_re_ri_posn': 1111,

                },
                'sun_roof_positions':{
                    'sun_roof_posn': 121,
                    'sun_roof_shade_posn':131
                }
            }
            nextev_message, obj = publish_msg('window_change_event', window_status=window_status)

            # 校验status_window表
            # check posn value were not stored
            window_status_in_mysql_new = checker.mysql.fetch('status_window',
                                                             {"id": vid, 'sample_time': timestamp_to_utc_strtime(obj['sample_ts'])},
                                                             exclude_fields=['update_time', 'sample_time'])[0]
            sun_roof_posn_sts_in_mysql = window_status_in_mysql_new.pop('sun_roof_posn_sts')
            assert_equal(window_status_in_mysql_old, window_status_in_mysql_new)

            # check sun_roof_posn_sts was stored
            assert_equal(sun_roof_posn_sts_in_mysql, obj['window_status']['sun_roof_positions']['sun_roof_posn_sts'])

    @pytest.mark.skip()
    def test_posn_out_100(self, checker, publish_msg):
        with allure.step("校验例外：win posn可以等于127，sun_roof_posn可为101，102，127"):
            # 上报
            window_status = {
                'window_positions':{
                    'win_frnt_le_posn':127,
                    'win_frnt_ri_posn':127,
                    'win_re_le_posn':127,
                    'win_re_ri_posn': 127,
                },
                'sun_roof_positions': {
                    'sun_roof_posn': random.choice([101,102,127])
                }
            }

            nextev_message, window_change_event_obj = publish_msg('window_change_event', window_status=window_status)

            # 校验
            tables = ['status_window']
            checker.check_mysql_tables(window_change_event_obj, tables)