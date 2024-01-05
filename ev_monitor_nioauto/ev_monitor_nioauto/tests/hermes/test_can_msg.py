#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/12/24 12:08
@contact: hongzhen.bi@nio.com
@description: 处理记录FCW（预测性碰撞报警系统/行人检测警报）及ABS（防抱死系统/紧急刹车）can信号功能，用于安全驾驶评分
"""
import time
import allure
import pytest


class TestCANMsg(object):
    @pytest.mark.skip("暂时关掉，待 cgw 上报指定信号后再后打开")
    def test_fcw_can(self, vid, publish_msg_by_kafka, mysql):
        signal_int = [
                {'name': 'RAD_FC_03:PCW_preWarning', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-AEB-2'}
            ]

        sample_ts = int(time.time())
        publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={"signal_int": signal_int}, sample_ts=sample_ts * 1000, sleep_time=3)
        with allure.step("校验数据统计库中的ubi_fcw_event表"):
            data = mysql['statistics'].fetch('ubi_fcw_event', where_model={'vehicle_id': vid, 'sample_time': sample_ts})
            assert data

    def test_abs_can(self, vid, publish_msg_by_kafka, mysql):
        """
        记录ABSActv从0到1的跳变
        """
        # 上报ABSActv=0
        can_msg = {
            'can_data': [
                {'msg_id': 94,
                 'value': b'\x00\x00\x00\x00\x00\x00\x00'}
            ]
        }
        publish_msg_by_kafka('alarm_signal_update_event', sample_points={"can_msg": can_msg})
        # 上报ABSActv=1
        can_msg = {
            'can_data': [
                {'msg_id': 94,
                 'value': b'\x90\x00\x00\x00\x00\x00\x00'}
            ]
        }
        sample_ts = int(time.time())
        publish_msg_by_kafka('alarm_signal_update_event', sample_points={"can_msg": can_msg}, sample_ts=sample_ts * 1000, sleep_time=3)
        with allure.step("校验数据统计库中的ubi_abs_event表"):
            data = mysql['statistics'].fetch('ubi_abs_event', where_model={'vehicle_id': vid, 'sample_time': sample_ts})
            assert data

    def test_abs_can_reissue(self, vid, publish_msg_by_kafka, mysql):
        """
        支持处理补发逻辑
        """
        now = int(time.time())
        with allure.step("上报ABSActv=0"):
            can_msg = {
                'can_data': [
                    {'msg_id': 94,
                     'value': b'\x00\x00\x00\x00\x00\x00\x00'}
                ]
            }
            publish_msg_by_kafka('alarm_signal_update_event', sample_points={"can_msg": can_msg}, sample_ts=now * 1000)

        with allure.step("间隔20s再次上报ABSActv=0"):
            can_msg = {
                'can_data': [
                    {'msg_id': 94,
                     'value': b'\x00\x00\x00\x00\x00\x00\x00'}
                ]
            }
            publish_msg_by_kafka('alarm_signal_update_event', sample_points={"can_msg": can_msg}, sample_ts=(now + 20) * 1000)
        with allure.step("上报ABSActv=1，时间戳在两次ABSActv=0之间"):
            can_msg = {
                'can_data': [
                    {'msg_id': 94,
                     'value': b'\x90\x00\x00\x00\x00\x00\x00'}
                ]
            }
            publish_msg_by_kafka('alarm_signal_update_event', sample_points={"can_msg": can_msg}, sample_ts=(now + 10) * 1000, sleep_time=3)
        with allure.step("校验数据统计库中的ubi_abs_event表"):
            data = mysql['statistics'].fetch('ubi_abs_event', where_model={'vehicle_id': vid, 'sample_time': (now + 10)})
            assert data