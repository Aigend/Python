#!/usr/bin/env python
# coding=utf-8
import pytest


class TestPowerSwapMsg(object):

    def test_power_swap_start_event(self, publish_msg_by_kafka, checker):
        # 上报
        nextev_message, obj = publish_msg_by_kafka('specific_event', event_type='power_swap_start')

        # 校验
        tables = ['vehicle_soc_history']
        checker.check_mysql_tables(obj, tables, sample_ts=obj['sample_ts'], event_name='power_swap_start')

    def test_power_swap_end_event(self, publish_msg_by_kafka, checker):
        # 换电结束时，是会上报power swap end或者failure中的一种
        nextev_message, obj = publish_msg_by_kafka('specific_event', event_type='power_swap_end')

        # 校验
        tables = ['vehicle_soc_history']
        checker.check_mysql_tables(obj, tables, sample_ts=obj['sample_ts'], event_name='power_swap_end')
