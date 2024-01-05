#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2021/06/01 10:58
@contact: hongzhen.bi@nio.com
"""
import json
import random


class TestPowerSwapLog(object):
    """
    车辆上报journey_start时,发现上报的nio_encoding和hermes缓存的不一致时,记录相关电池变更信息的log到over_see_event_power_swap
    """

    def test_power_swap_log(self, cmdopt, vid, mysql, redis, publish_msg_by_kafka):
        btry_id = ['SQETEST0999647340000000000DDtest', 'SQETEST0999647340000000000DStest']
        cache = redis['datacollection'].get(f"hermes_{cmdopt}:oversee_persist_monitor_item_PowerSwapActor_{vid}")
        old_btry_data = json.loads(cache)
        old_btry = old_btry_data['batIdAfter']
        if old_btry in btry_id:
            btry_id.remove(old_btry)
            new_btry = btry_id[0]
        else:
            new_btry = random.choice(btry_id)

        publish_msg_by_kafka('journey_start_event',
                             battery_package_info={
                                 "btry_pak_encoding": [
                                     {
                                         "btry_pak_sn": 1,
                                         "nio_encoding": new_btry,
                                         "re_encoding": "OHN291708YTFS4ABCU6XJZQPG5RVKMEL"
                                     }
                                 ]
                             }, sleep_time=5)

        log_mysql = mysql['rvs'].fetch('over_see_event_power_swap', {"vehicle_id": vid}, order_by='id desc limit 1')[0]
        assert log_mysql['chg_subsys_encoding_before'] != new_btry
        assert log_mysql['chg_subsys_encoding_after'] == new_btry
