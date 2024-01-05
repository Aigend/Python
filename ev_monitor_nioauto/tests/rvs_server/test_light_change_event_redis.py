#!/usr/bin/env python
# coding=utf-8


class TestLightChangeMsg(object):
    def test_light_change_event_redis(self, checker, publish_msg_by_kafka):
        # 构造并上报消息
        nextev_message, light_change_obj = publish_msg_by_kafka('light_change_event')

        # 校验
        keys = ['LightStatus']
        checker.check_redis(light_change_obj, keys, event_name='light_change_event',sample_ts=light_change_obj['sample_ts'])
