#!/usr/bin/env python
# coding=utf-8
import pytest

from utils.time_parse import timestamp_to_utc_strtime


@pytest.mark.skip("不再存储status_nbs")
class TestNBSStatusChangeMsg(object):
    def test_nbs_status_change_event_mysql(self, checker, publish_msg):
        # 构造并上报消息
        nextev_message, nbs_change_obj = publish_msg('nbs_status_change_event')

        # 校验
        tables = ['status_nbs']
        checker.check_mysql_tables(nbs_change_obj, tables)

    def test_nbs_abort_reason_large_wont_save(self, vid, publish_msg, checker):
        # 获取原有nbs_abort_reason
        nbs_abort_reason = checker.mysql.fetch_one('status_nbs', {"id": vid}, order_by='id desc')['nbs_abort_reason']

        # 构造并上报消息
        nextev_message, obj = publish_msg('nbs_status_change_event', nbs_status={'nbs_abort_reason': 256})

        # 校验mysql没保存
        sample_ts = obj['sample_ts']
        sample_time = timestamp_to_utc_strtime(sample_ts)
        res = checker.mysql.fetch('status_nbs', {"id": vid, 'sample_time': sample_time})
        assert res[0]['nbs_abort_reason'] == nbs_abort_reason

    def test_nbs_abort_reason_negative_wont_save(self, vid, publish_msg, checker):
        # 获取原有nbs_abort_reason
        nbs_abort_reason = checker.mysql.fetch_one('status_nbs', {"id": vid}, order_by='id desc')['nbs_abort_reason']

        # 构造并上报消息
        nextev_message, obj = publish_msg('nbs_status_change_event', nbs_status={'nbs_abort_reason': -1})

        # 校验mysql没保存
        sample_ts = obj['sample_ts']
        sample_time = timestamp_to_utc_strtime(sample_ts)
        res = checker.mysql.fetch('status_nbs', {"id": vid, 'sample_time': sample_time})
        assert res[0]['nbs_abort_reason'] == nbs_abort_reason
