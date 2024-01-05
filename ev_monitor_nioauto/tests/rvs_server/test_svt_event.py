#!/usr/bin/env python
# coding=utf-8

import json
import allure
import pytest

from utils.assertions import assert_equal

# TODO 马克波罗服务暂不支持，先跳过
@pytest.mark.marcopolo_skip
class TestSvtEventMsg(object):
    def test_svt_event(self, vid, publish_msg, checker, kafka):
        """
        SVT confluence：https://confluence.nioint.com/pages/viewpage.action?pageId=161468424
        SVT PRD：https://confluence.nioint.com/display/CVS/Stolen+Vehicle+Tracking
        只有当车辆为激活状态且上报的reason_code为：
            1、lv_bat_removal_on
            2、gnss_ant_fault_on
            3、anti_theft_alarm_on
            4、unauth_movement_on
        这四种情况时，才会推送app和SCR
        """
        kafka['cvs'].set_offset_to_end(kafka['topics']['push_event'])

        # 上报
        nextev_message, obj = publish_msg('svt_event')

        with allure.step('校验kafka {}'.format(kafka['topics']['push_event'])):
            is_found = False
            for data in kafka['cvs'].consume(kafka['topics']['push_event'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['data']['sample_time'] == obj['sample_ts']//1000 and vid == kafka_msg['vehicle_id']:
                    is_found = True
                    break
            assert_equal(True, is_found)

        with allure.step('校验mysql'):
            tables = ['svt_event']
            checker.check_mysql_tables(obj, tables, sample_ts=obj['sample_ts'])

