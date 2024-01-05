#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/08/31 14:38
@contact: hongzhen.bi@nio.com
@description: config result和command result均可以处理rvs_wlan_config命令
"""

class TestConfigWlan(object):
    def test_config_wlan(self):
        """
        车辆在线 执行https://tsp-test-int.nio.com:4430/api/1/in/vehicle/command/config_wlan。

        1、使车辆按照 generic_config_result_pb2 的格式返回执行结果，查询 control_online_commmand 表，执行成功。

        2、使车辆按照 cmd_result_pb2 的格式返回执行结果，查询 control_online_commmand 表，执行成功。
        """
        pass