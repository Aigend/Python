#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2021/06/01 14:02
@contact: hongzhen.bi@nio.com
"""
import json


class TestIccidLog(object):
    """
    车辆上报journey_start时,发现上报的iccid和hermes缓存不一样时,期望可以记录相关的iccid变更的log到over_see_event_iccid_change
    """

    def test_iccid_log(self, cmdopt, vid, mysql, redis, publish_msg_by_kafka):
        icc_id = ['ICCSQETEST0999647340', 'ICCSQETEST099964test']
        cache = redis['datacollection'].get(f"hermes_{cmdopt}:oversee_persist_monitor_item_IccidChangeActor_{vid}")
        old_iccid_data = json.loads(cache)
        old_iccid = old_iccid_data['iccidAfter']
        icc_id.remove(old_iccid)
        new_iccid = icc_id[0]

        publish_msg_by_kafka('journey_start_event', icc_id=new_iccid, sleep_time=10)

        log_mysql = mysql['rvs'].fetch('over_see_event_iccid_change', {"vehicle_id": vid}, order_by='id desc limit 1')[0]
        assert log_mysql['iccid_before'] == old_iccid
        assert log_mysql['iccid_after'] == new_iccid
