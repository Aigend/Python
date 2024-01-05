#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2021/04/29 16:48
@contact: hongzhen.bi@nio.com
@description: 断网告警监控
"""
import time
import pytest


class TestConnectionStatusMonitor(object):
    # @pytest.mark.skip('manual')
    def test_connection_status_monitor(self, mysql):
        """
        断网告警监控
        每30秒查询一次 vds.connection_count_new(该表每分钟统计一次)，计算断网百分比

        存时间戳的redis key：hermes_test:ConnectionCount_key

        该功能的配置项存在 hermes 数据库中的 over_see_config 表，每30秒加载一次
        rule_name=ConnectionCountActor，value举例如下
        {"param_map":{"sms_enable":"false","sms_to":"15901558284,15201181753","time_step":"500","threshold":"92"}}
        sms_enable：是否开启短信发送
        sms_to：告警短信发送给谁
        time_step：短信每隔多少秒推送一次
        threshold：CGW在线率小于该百分位则推送短信告警
        """

        mysql['hermes'].update('over_see_config',
                               where_model={"rule_name": "ConnectionCountActor"},
                               fields_with_data={"config": '{"param_map":{"sms_enable":"true","sms_to":"15911051120,13552120960","time_step":"20","threshold":"100"}}',
                                                 "update_time": int(time.time())})

        time.sleep(31)

        mysql['hermes'].update('over_see_config',
                               where_model={"rule_name": "ConnectionCountActor"},
                               fields_with_data={"config": '{"param_map":{"sms_enable":"false","sms_to":"15901558284,15201181753","time_step":"500","threshold":"92"}}',
                                                 "update_time": int(time.time())})
