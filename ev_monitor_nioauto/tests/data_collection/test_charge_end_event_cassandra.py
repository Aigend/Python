#!/usr/bin/env python
# coding=utf-8

"""
:file: test_charge_end_event_cassandra.py
:author: chunming.liu
:Date: Created on 2019/1/8 下午5:04
:Description: 充电结束消息存储到Cassandra的vehicle_data中。
1）上报mileage比cassandra原来小，会更新到cassandra
2）posng_invalid_type=1\2时，cassandra中的position_status字段要更新，但是目前CGW此时不会上传position数据。
"""


class TestChargeEndMsg(object):
    def test_charge_end_event_cassandra(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, charge_end_obj = publish_msg('charge_end_event')

        # 校验
        tables ={'vehicle_data':['vehicle_id',
                                 'charging_info',
                                 'soc_status',
                                 'position_status',
                                 'vehicle_status',
                                 'process_id as charge_id',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(charge_end_obj, tables, event_name='charge_end_event')

