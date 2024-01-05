#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/07/20 11:53
@contact: hongzhen.bi@nio.com
@description: 充电补偿逻辑
"""
import json
import time

import allure

from utils.assertions import assert_equal


class TestFillFieldFromRedisCharge(object):
    def test_charge_update_redis(self, env, vid, redis_key_front, checker, publish_msg_by_kafka):
        """
        1.  消费 periodical_charge_update 事件， 在redis里记录此次charge的第一条记录和最后一条记录
            (key:  remote_vehicle_test:charge_first  remote_vehicle_test:charge_last)，
            当charge_start/charge_end 丢失数据时候(缺soc/dump_energy等 vehicle_charge_history需要的数据)，用redis的数据补
            redis缓存数据的ttl为72小时

        2.  只有第一次充电更新才会更新 charg_first 对应event_id的值，每一次充电更新都会更新redis中对应charge_last对应event_id的值

        3.  当丢失charge_start 或者charge_end时候，利用redis中存的first/last数据，来补偿此次丢失,
            在每天的 02:00 和 14:00 进行数据补偿， 补偿 vehicle_soc_history create_time 在(12h, 24h) 之间的数据丢失情况。
        """
        charge_id = int(time.time())
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        # 清除redis 缓存
        key_first = f'{remote_vehicle_key_front}:charge_first:{vid}:{charge_id}'
        key_last = f'{remote_vehicle_key_front}:charge_last:{vid}:{charge_id}'
        checker.redis.delete(key_first)
        checker.redis.delete(key_last)

        with allure.step("不论是否上报行程开始，还是行程结束，只要上报行程更新，redis中就会缓存该行程数据"):
            publish_msg_by_kafka('periodical_charge_update', charge_id=str(charge_id))
            assert_equal(bool(checker.redis.get(key_first)), True)
            assert_equal(bool(checker.redis.get(key_last)), True)

    def test_socstatus_in_vehicle_status(self, vid, redis_key_front, checker, publish_msg):
        """
        redis中vehicle_status电量SocStatus状态补充逻辑
        """
        with allure.step("校验redis中有SocStatus时，上报charge_start_event，SocStatus会更新"):
            # 清除redis 缓存
            remote_vehicle_redis_key_front = redis_key_front['remote_vehicle']
            checker.redis.delete(f'{remote_vehicle_redis_key_front}:vehicle_status:{vid}:SocStatus')

            # 上报充电开始，使redis中有值
            publish_msg('charge_start_event')
            # 第二次上报充电开始，redis值会更新
            nextev_message, charge_start_obj = publish_msg('charge_start_event')
            # 校验
            checker.check_redis(charge_start_obj, ['SocStatus'], event_name='charge_start_event', clear_none=True)

        with allure.step(
                "校验redis中有socstatus时，上报periodical_charge_update，若上报数据中无chargingInfo和nio_encoding则补充更新前数据，其他数据更新"):
            original_redis = json.loads(checker.redis.get(f'{remote_vehicle_redis_key_front}:vehicle_status:{vid}:SocStatus'))
            battery_package_info = {'btry_pak_encoding': [{'nio_encoding': original_redis['battery_id']}]}
            charging_info = {
                'estimate_chrg_time': original_redis['estimate_charge_time'],
                'charger_type': original_redis['charger_type'],
                'in_volt_ac': original_redis['in_volt_ac'],
                'in_volt_dc': original_redis['in_volt_dc'],
                'in_curnt_ac': original_redis['in_curnt_ac']
            }
            nextev_message, charge_update_obj = publish_msg('periodical_charge_update',
                                                            clear_fields=["sample_points[0].charging_info",
                                                                          "sample_points[0].can_msg",
                                                                          "sample_points[0].alarm_signal"])
            charge_update_obj['sample_points'][0]['battery_package_info'] = battery_package_info
            charge_update_obj['sample_points'][0]['charging_info'] = charging_info
            # 校验
            checker.check_redis(charge_update_obj['sample_points'][0], ['SocStatus'], event_name='charge_update_event',
                                clear_none=True)

        with allure.step("校验redis中有SocStatus时，上报charge_end_event，若上报数据中无chargingInfo和nio_encoding则补充更新前数据，其他数据更新"):
            nextev_message, charge_end_obj = publish_msg('charge_end_event', clear_fields=['charging_info'])
            charge_end_obj['battery_package_info'] = battery_package_info
            charge_end_obj['charging_info'] = charging_info
            checker.check_redis(charge_end_obj, ['SocStatus'], event_name='charge_end_event', clear_none=True)

        with allure.step(
                "校验redis中有socstatus时，上报journey_start_event，若redis中上报数据中无chargingInfo和nio_encoding则补充更新前数据，其他数据更新"):
            nextev_message, journey_start_obj = publish_msg('journey_start_event',
                                                            clear_fields=['battery_package_info'])
            journey_start_obj['battery_package_info'] = battery_package_info
            journey_start_obj['charging_info'] = charging_info
            checker.check_redis(journey_start_obj, ['SocStatus'], event_name='journey_start_event', clear_none=True)

        with allure.step(
                "校验redis中有socstatus时，上报periodical_journey_update，若redis中上报数据中无chargingInfo和nio_encoding则补充更新前数据，其他数据更新"):
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update',
                                                             clear_fields=["sample_points[0].alarm_signal",
                                                                           "sample_points[0].can_msg"])
            journey_update_obj['sample_points'][0]['battery_package_info'] = battery_package_info
            journey_update_obj['sample_points'][0]['charging_info'] = charging_info
            checker.check_redis(journey_update_obj['sample_points'][0], ['SocStatus'],
                                event_name='journey_update_event', clear_none=True)

        with allure.step("校验redis中有SocStatus时，上报journey_end_event，若上报数据中无chargingInfo和nio_encoding则补充更新前数据，其他数据更新"):
            nextev_message, journey_end_obj = publish_msg('journey_end_event')
            journey_end_obj['battery_package_info'] = battery_package_info
            journey_end_obj['charging_info'] = charging_info
            checker.check_redis(journey_end_obj, ['SocStatus'], event_name='journey_end_event', clear_none=True)
