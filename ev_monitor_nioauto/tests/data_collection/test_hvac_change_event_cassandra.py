#!/usr/bin/env python
# coding=utf-8

"""
:file: test_rvs_events_report_event_cassandra.py
:author: muhan.chen
:Date: Created on 2018/5/14 下午3:25
:Description: 空调数据上报存储到cassandra的vehicle_data
"""

import pytest

case = [
    'air_con_on=0 and ccu_cbn_pre_ac_ena_sts=1, result mysql air_con_on=1, hvac on',
    'air_con_on=1 and ccu_cbn_pre_ac_ena_sts=0, result mysql air_con_on=1, hvac on',
    'air_con_on=1 and ccu_cbn_pre_ac_ena_sts=1, result mysql air_con_on=1, hvac on',
    'air_con_on=0 and ccu_cbn_pre_ac_ena_sts=0, result mysql air_con_on=0, hvac off'
]


class TestHvacChangeMsg(object):
    @pytest.mark.parametrize("air_con_on,ccu_cbn_pre_ac_ena_sts", zip([0, 1, 1, 0], [1, 0, 1, 0]), ids=case)
    def test_hvac_change_event_cassandra(self, air_con_on, ccu_cbn_pre_ac_ena_sts, publish_msg, checker):
        # 构造并上报消息
        nextev_message, hvac_change_obj = publish_msg('hvac_change_event',
                                                      hvac_status={"air_con_on": air_con_on,
                                                                   "ccu_cbn_pre_ac_ena_sts": ccu_cbn_pre_ac_ena_sts}
                                                      )

        # 校验
        tables ={'vehicle_data':['vehicle_id',
                                 'hvac_status',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(hvac_change_obj, tables, event_name='hvac_change_event')
