#!/usr/bin/env python
# coding=utf-8


class TestWindowChangeMsg(object):
    def test_window_change_event_redis(self, checker, publish_msg_by_kafka):
        # 构造并上报消息
        nextev_message, window_change_obj = publish_msg_by_kafka('window_change_event')

        # 校验
        keys = ['WindowStatus']
        checker.check_redis(window_change_obj, keys, event_name='window_change_event', sample_ts=window_change_obj['sample_ts'])