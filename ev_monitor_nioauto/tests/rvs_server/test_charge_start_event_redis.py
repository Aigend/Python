#!/usr/bin/env python
# coding=utf-8

"""
:file:
:author: yry
:Date: Created on 2016/11/11
:Description: 充电开始事件
"""
import time

import pytest
import allure
import json
from utils.assertions import assert_equal


class TestChargeStartMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, mysql):
        original_mileage_in_mysql = mysql['rvs'].fetch('status_vehicle',
                                                       {"id": vid
                                                        },
                                                       ['mileage']
                                                       )[0]['mileage']

        return {'original_mileage': original_mileage_in_mysql}


    @pytest.mark.marcopolo_skip
    def test_charge_start_event(self, vid, publish_msg, checker, prepare, redis_key_front):
        # 马克波罗服务需要跳过@pytest.mark.skip('marcopolo app server')
        # 清除redis 缓存
        signals = []
        flag = 0 #random.choice([0, 1])
        can_ids = [537, 590, 623, 80, 617]
        for ii in can_ids:
            signal = {'id': ii, 'data_info': []}
            for i in range(2):
                if i == flag:
                    signal['data_info'].append({'ts_offset': i, 'data': '0000000000000000'})
                else:
                    signal['data_info'].append({'ts_offset': i, 'data': '1111111111111111'})
            signals.append(signal)
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        for key in ['PositionStatus', 'SocStatus', 'ExteriorStatus']:
            checker.redis.delete(f'{remote_vehicle_key_front}:vehicle_status:{vid}:{key}')
        """
        当充电事件push到app后，会往redis的charge_push_xxx_start/charge_push_xxx_end 记录一个sample_ts.
        如果该key有值了，就认为该event_id对应的充电事件已经推送过，不再往APP推送。
        当sample_ts与当前时间比较超过10分钟的话，不再往APP做推送，同时也不更新charge_push_xxx_start/charge_push_xxx_end

        redis往charge_push:{vid}:{event_id}:start key存数据时，会进行一个判断，
        如果mysql的vehicle_soc_history表的end_time字段值=1970***(0)，则认为充电事件未完成，此时会存储新值
        如果>0时，则认为充电事件已然完成，此时不会存储新值。

        此处我们设置 charge_ID(即event_id)值，是因为test_charge_end_redis case 在此case之前，
        已然往ehicle_soc_history落库了end_time>0.故redis不会存储相同的event_id的start的值。
        """
        charge_id = time.strftime("%Y%m%d%M%S", time.localtime())
        # 在充电开始之后等待1分钟，再根据车辆状态数据向车辆主用车人推送充电提醒。如果1分钟时已停止充电，则不再提醒。
        sample_ts = int(round(time.time() * 1000)) - 1 * 60 * 1000
        # 构造并上报 charge_start 事件消息
        soc = 10
        nextev_message, charge_start_obj = publish_msg('charge_start_event', charge_id=charge_id, sample_ts=sample_ts,
                                                       vehicle_status={"mileage": prepare['original_mileage'], 'soc': soc},
                                                       # 当SoC>90%时，不推送开始充电的消息，也不推送此次充电结束的消息
                                                       soc_status={'soc': soc})
        # 校验 charge_start 事件落入Redis库
        keys = ['PositionStatus', 'SocStatus']
        checker.check_redis(charge_start_obj, keys, event_name='charge_start_event', clear_none=True)
        # 上报 periodical_charge_update 事件
        time.sleep(2)
        nextev_message, charge_update_obj = publish_msg('periodical_charge_update', charge_id=charge_id,
                                                        sample_points=[{'vehicle_status': {"mileage": prepare['original_mileage'], 'soc': soc+1}, "soc_status": {'soc': soc+1},
                                                                        'can_signal': {"signal_info": signals}},

                                                                        ],
                                                        clear_fields=['sample_points[0].can_msg',
                                                                      'sample_points[0].charging_info',
                                                                      'sample_points[0].tyre_status',
                                                                      'sample_points[0].occupant_status']
                                                        )
        # 校验 charge_push 的Redis
        # 车辆处于维修模式，charge_push的redis不会落库。应确保上报的ntester=false，且mysql中的维修工单vehicle_repair_order表的order_status_code为10。
        keys = ['charge_push_start.{event}'.format(event=charge_update_obj['charge_id'])]  # event为充电的event_id
        checker.check_redis(charge_update_obj, keys, event_name='charge_start_event', clear_none=True)

    def test_charge_event_wont_push(self, vid, publish_msg, checker, prepare, redis_key_front):
        """
        当SoC>90%时，不推送开始充电的消息，也不推送此次充电结束的消息
        """
        charge_id = time.strftime("%Y%m%d%M%S", time.localtime())
        # 清除redis 缓存
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        key_start = f'{remote_vehicle_key_front}:charge_push:{vid}:{charge_id}:start'
        key_end = f'{remote_vehicle_key_front}:charge_push:{vid}:{charge_id}:end'
        checker.redis.delete(key_start)
        checker.redis.delete(key_end)
        # 在充电开始之后等待2分钟，再根据车辆状态数据向车辆主用车人推送充电提醒。如果两分钟时已停止充电，则不再提醒。
        sample_ts = int(round(time.time() * 1000)) - 3 * 60 * 1000
        # 构造并上报 charge_start 事件消息
        publish_msg('charge_start_event', charge_id=charge_id, sample_ts=sample_ts,
                    vehicle_status={"mileage": prepare['original_mileage'] + 1},
                    soc_status={'soc': 91})
        with allure.step("当SoC>90%时，不推送开始充电的消息"):
            # 上报 periodical_charge_update 事件
            time.sleep(2)
            publish_msg('periodical_charge_update', charge_id=charge_id,
                        sample_points=[{'vehicle_status': {"mileage": prepare['original_mileage'] + 2}}])
            assert_equal(bool(checker.redis.get(key_start)), False)
        with allure.step("也不推送此次充电结束的消息"):
            publish_msg('charge_end_event', charge_id=charge_id,
                        vehicle_status={"mileage": prepare['original_mileage'] + 3},
                        soc_status={'soc': 98})
            assert_equal(bool(checker.redis.get(key_end)), False)

    def test_charge_start_soc_is_0_redis_is_0(self, checker, publish_msg, prepare):
        with allure.step("校验充电开始事件，即上报soc=0，查看redis中对应数据更新为0"):
            nextev_message, charge_start_event_obj = publish_msg('charge_start_event', soc_status={'soc': 0}, vehicle_status={"mileage": prepare['original_mileage'] + 1}, sleep_time=5)
            # 校验
            keys = ['SocStatus']
            checker.check_redis(charge_start_event_obj, keys, event_name='charge_start_event', clear_none=True)

    def test_charge_start_position(self, checker, publish_msg, prepare, redis_key_front, vid, redis):
        with allure.step("校验充电开始事件，上报position中 gps_time小于redis中存储的sampletime-gps time>24h，redis中数据不更新"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            redis_key = remote_vehicle_key_front + ':vehicle_status:' + vid + ':PositionStatus'
            redis_value_before = json.loads(redis['cluster'].get(redis_key))
            nextev_message, charge_start_event_obj = publish_msg('charge_start_event',
                                                                 position_status={'gps_ts': redis_value_before['gps_time'] - 25 * 3600 * 1000},
                                                                 vehicle_status={
                                                                     "mileage": prepare['original_mileage'] + 1}
                                                                 )

            # 校验

            redis_value_after = json.loads(redis['cluster'].get(redis_key))
            assert_equal(redis_value_after, redis_value_before)

    def test_nio_encoding_31(self, checker, publish_msg, redis_key_front, vid, redis, vin):
        with allure.step("校验nio_encoding为31位时（31位的nio_encoding后面会补一位空格上报），在写redis之前删除空格"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            redis_key = remote_vehicle_key_front + ':vehicle_status:' + vid + ':SocStatus'

            # 31位的nio_encoding后面会补一位空格上报
            nio_encoding = f'{vin}00000000DDtest '
            nextev_message, charge_start_event_obj = publish_msg('charge_start_event',
                                                                 battery_package_info={
                                                                     "btry_pak_encoding": [
                                                                         {
                                                                             "btry_pak_sn": 1,
                                                                             "nio_encoding": nio_encoding,
                                                                         }
                                                                     ],
                                                                 }
                                                                 )

            # 校验
            redis_value_after = json.loads(redis['cluster'].get(redis_key))
            assert_equal(redis_value_after['battery_id'], nio_encoding[:-1])

    @pytest.mark.skip("Manual")
    def test_charge_push_display(self, vid, redis_key_front, publish_msg_by_kafka, checker, prepare):
        """
        1、如果充电类型是交流充电，并且车门未锁时，开始充电推送文案”爱车(*车辆昵称/车牌后四位*)充电已开始，当前电量 x%，预计{y}充满，锁车会提升交流充电的速度“
            - 有昵称显示昵称，
            - 无昵称有车牌显示车牌后四位，
            - 无昵称无车牌只推送"爱车充电已开始...."
            - 充电结束的昵称显示遵循同样的规则
        2、如果充电类型是直流充电或交流车门上锁时，开始充电推送文案”充电已开始，当前电量 x%，预计{y}充满“
        3、如果充电开始/结束数据是补发数据，且补发时间距离当前超过10分钟，则对应开始充电的提醒就不必再发送了。
        4、如果充电开始数据滞后于对应的充电结束数据，那么该充电开始的提醒就不必再发送了。
        5、充电开始/结束，同一充电事件(event_id)只推送一次消息给app
        """
        charge_id = time.strftime("%Y%m%d%M%S", time.localtime())
        # 清除redis 缓存
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        key_start = f'{remote_vehicle_key_front}:charge_push:{vid}:{charge_id}:start'
        checker.redis.delete(key_start)

        sample_ts = int(round(time.time() * 1000)) - 3 * 60 * 1000
        # 上报车门状态
        publish_msg_by_kafka('door_change_event', door_status={'door_lock_frnt_le_sts': 0,
                                                               'door_lock_frnt_ri_sts': 0,
                                                               'vehicle_lock_status': 0})
        # 上报充电开始 charger_type: 2-AC, 3-DC
        charger_type = 2
        publish_msg_by_kafka('charge_start_event', charge_id=charge_id, sample_ts=sample_ts,
                             charging_info={'charger_type': charger_type})

        publish_msg_by_kafka('periodical_charge_update', charge_id=charge_id,
                             sample_points=[{'charging_info': {'charger_type': charger_type}}])

        publish_msg_by_kafka('charge_end_event', charge_id=charge_id,
                             charging_info={'charger_type': charger_type})
