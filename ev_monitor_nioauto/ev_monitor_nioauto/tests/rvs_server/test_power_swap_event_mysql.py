#!/usr/bin/env python
# coding=utf-8
import pytest


@pytest.mark.skip("merged in kafka cases")
class TestPowerSwapMsg(object):
    # @pytest.mark.skip('stg')  # 此测试用例在校验经纬度字段时需先调用查询当前最新路径信息接口，该接口在stg环境强制签名校验，故略过。
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

    def test_power_swap_failure_event(self, publish_msg_by_kafka, checker):
        # 换电结束时，是会上报power swap end或者failure中的一种
        # 注意，目前的逻辑确是多次上报同一个event_id只存第一次的fail reason
        nextev_message, obj = publish_msg_by_kafka('specific_event', event_type='power_swap_failure')

        # 校验
        tables = ['vehicle_soc_history']
        checker.check_mysql_tables(obj, tables, sample_ts=obj['sample_ts'], event_name='power_swap_failure')
