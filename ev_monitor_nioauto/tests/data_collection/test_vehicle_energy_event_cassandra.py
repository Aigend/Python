#!/usr/bin/env python
# coding=utf-8


class TestVehicleEnergyMsg(object):
    def test_vehicle_energy_event_cassandra(self, publish_msg_by_kafka, checker):
        # 构造并上报消息
        nextev_message, vehicle_energy_event_obj = publish_msg_by_kafka('vehicle_energy_event')

        # 校验
        tables = {'vehicle_data': ['vehicle_id',
                                   'vehicle_energy_status',
                                   'sample_ts']}

        checker.check_cassandra_tables(vehicle_energy_event_obj, tables, event_name='vehicle_energy_event')

