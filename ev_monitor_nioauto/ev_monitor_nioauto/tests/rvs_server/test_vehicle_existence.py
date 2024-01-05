#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/08/31 13:43
@contact: hongzhen.bi@nio.com
@description:   车辆在线环境记录,
                用于标记车辆是在prod/stg环境连接消息,
                便于查看车辆当前连接的那个环境,
                统计记录保存remote_vehicel_test.vehicle_existence表
"""
from utils.assertions import assert_equal


class TestVehicleExistence(object):
    def test_vehicle_existence(self, vid, cmdopt, publish_msg, mysql):
        """
        dev(stg)上线的车辆可以记录到test(prod)表并标记为stg环境
        test(prod)上线的车辆可以记录到test(prod)表并标记为prod环境
        """
        if cmdopt == 'stg':
            pass
        else:
            original_vehicle_existence = mysql['rvs'].fetch('vehicle_existence', {'id': vid})[0]
            publish_msg('light_change_event')
            vehicle_existence = mysql['rvs'].fetch('vehicle_existence', {'id': vid})[0]
            assert_equal(vehicle_existence['current_env'], "PROD")
            assert_equal(vehicle_existence['current_env'] != original_vehicle_existence['update_time'], True)
