#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2022/05/10 16:57
@contact: hongzhen.bi@nio.com
"""
import time

import pytest


class TestEnvComfortEvent(object):
    @pytest.mark.parametrize('event_type', ['air_conditioner_event', 'steer_wheel_heating_event', 'seat_heating_event', 'seat_ventilation_event'])
    def test_env_comfort_event(self, vid, publish_msg, event_type, redis):
        """
        PRD: https://nio.feishu.cn/wiki/wikcnqfNATzd7QWgn4ZUjPsmbbf?useNewLarklet=1
        specific_event: https://nio.feishu.cn/docs/doccnOprvKN0WuQX728hJB6qw8r

        configmap配置项: env_comfort.push.switch=true

        前置条件: 车辆已激活、不在维修中、不在升级中

        event_detail = 'soc_low' 则推送 APP

        redis key: hermes_test:comfort_push:{vid}:{event_type}:{sample_ts}
        """
        sample_ts = int(round(time.time() * 1000))
        data = {'event_detail': 'soc_low', 'sample_ts': sample_ts}
        publish_msg('specific_event', event_type=event_type, data=data)

        assert redis['cluster'].get(f'hermes_test:comfort_push:{vid}:{event_type}:{sample_ts}')
