#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2021/02/23 14:29
@contact: hongzhen.bi@nio.com
@description: 状态推送——车门、窗、大灯状态监控提醒
@showdoc: http://showdoc.nevint.com/index.php?s=/150&page_id=4492
"""
import time

import allure
import pytest

from nio_messages.nextev_msg import gen_nextev_message


class TestStatusPush():
    @pytest.fixture(scope="function")
    def prepare(self, env, cmdopt, vin, vid, kafka, publish_msg_by_kafka):
        vehicles = [
            (vid, vin, 'ES8'),
            (env['vehicles']['ET7_not_active']['vehicle_id'], env['vehicles']['ET7_not_active']['vin'], 'ET7'),
            (env['vehicles']['ET7_active']['vehicle_id'], env['vehicles']['ET7_active']['vin'], 'ET7')
        ]
        with allure.step("上报connection事件"):
            ts = int(time.time() * 1000)
            for vehicle in vehicles:
                # 上报车辆在线
                msg = gen_nextev_message("connection_status_event", {"status": 'ONLINE'}, publish_ts=ts, msg_type=4, account_id=vehicle[0])
                kafka['cvs'].produce(kafka['topics']['cgw'], msg)

                # 预置车辆状态
                # 车内无人
                occupant_status = {'fr_le_seat_occupant_status': 0, 'fr_ri_seat_occupant_status': 0}
                # 车辆状态为停车未充电
                vehicle_status = {'vehl_state': 2, 'chrg_state': 3, 'comf_ena': 0}
                position_status = {'posng_valid_type': 0, 'longitude': 121.386645, 'latitude': 31.164862}
                soc_status = {'chrg_state': 0, 'soc': 66.6, 'remaining_range': 30}
                # 关闭所有车门
                door_status = {
                    "charge_port_status": [
                        {
                            "ajar_status": 1,
                            "charge_port_sn": 0
                        },
                        {
                            "ajar_status": 1,
                            "charge_port_sn": 1
                        }
                    ],
                    "door_ajars": {
                        "door_ajar_frnt_le_sts": 1,
                        "door_ajar_frnt_ri_sts": 1,
                        "door_ajar_re_le_sts": 1,
                        "door_ajar_re_ri_sts": 1
                    },
                    "door_locks": {
                        "access_mode": 30,
                        "door_lock_frnt_le_sts": 1,
                        "door_lock_frnt_ri_sts": 1,
                        "entry_meth": 1,
                        "user_id": 2602
                    },
                    "engine_hood_status": {
                        "ajar_status": 1
                    },
                    "tailgate_status": {
                        "ajar_status": 1
                    },
                    "vehicle_lock_status": 1
                }
                # 关闭所有车窗
                window_status = {
                    "sun_roof_positions": {
                        "sun_roof_posn": 0,
                        "sun_roof_shade_posn": 0,
                        "sun_roof_posn_sts": 0
                    },
                    "window_positions": {
                        "win_frnt_le_posn": 0,
                        "win_frnt_ri_posn": 0,
                        "win_re_le_posn": 0,
                        "win_re_ri_posn": 0,
                    }
                }
                window_status['sun_roof_positions']['sun_roof_posn'] = 101 if vehicle[2] in ['ES6', 'ET7', 'ET5'] else 0
                window_status['sun_roof_positions']['sun_roof_posn_sts'] = 4 if vehicle[2] == 'ES8' else 0
                # 关闭空调
                hvac_status = {
                    "air_con_on": 0,
                    "amb_temp_c": -26.5,
                    "outside_temp_c": 22.0,
                    "pm_2p5_cabin": 19,
                    "pm_2p5_filter_active": 0,
                    "cbn_pre_sts": 0,
                    "ccu_cbn_pre_aqs_ena_sts": 0
                }
                publish_msg_by_kafka('instant_status_resp', vid=vehicle[0], vin=vehicle[1],
                                     sample_point={
                                         "vehicle_status": vehicle_status,
                                         "position_status": position_status,
                                         "soc_status": soc_status,
                                         "door_status": door_status,
                                         "window_status": window_status,
                                         "hvac_status": hvac_status,
                                         "occupant_status": occupant_status
                                     }, sleep_time=2)

    def test_status_push(self, env, cmdopt, vid, publish_msg_by_kafka, prepare, redis):
        """
        当车辆上报了非关闭状态的door_change_event、window_change_event、light_change_event后
        Hermes将事件中的时间戳加10分钟，写入Hermes库的status_push表中的push_time
        十分钟后(hermes每10s查一次)，到了push_time的时间，Hermes查询所有redis的Status状态，如果有处于未关闭的，则push提醒
        推送记录保存在push_log表中

        get remote_vehicle_test:vehicle_status:{vid}:WindowStatus
        get remote_vehicle_test:vehicle_status:{vid}:DoorStatus

        前置条件：
        1、车辆停泊vehicle_state = 2 且 comf_ena = 0
            get hermes_test:vehl_status:74361e94a61846e2a690d2e2a9bf591d:VehicleStatus
        3、车辆在线
            get hermes_test:vehl_status:{vid}:ConnectionStatus
        4、维修状态时不推送
            get hermes_test:vehl_status:{vid}:VehicleStatus  # 查询ntester
            get remote_vehicle_test:vehicle_status:{vid}:SpecialStatus  # 查询repaired
        5、车辆未激活不推送
        6、用户能够设置不推送 (记录在rvs库的vehicle_push_switch表)

        注意：
        1、定时器初始化为10分钟，如果门窗锁等状态发生改变，则定时器需要重新初始化。
        2、若车辆驻车状态或者主副驾无人的状态发生了改变，定时器将被关闭。
        3、推送后记录redis：get hermes_test:compo_push_feedback:{vid}:{push_time}，如果该key存在该状态的记录则不推送


        NT2未锁车提醒需求设计文档: https://nio.feishu.cn/docs/doccnXHKMrtSik1ScgJpks3tU1e
        NT2检测到用户未锁车，10min后，不推送APP，而是给车主发送短信提示，若30min后用户仍未锁车，给车主拨打语音电话提醒。
        短信提示文案：检测到爱车车门尚未上锁，请留意
        语音电话文案：你好。蔚来汽车给您来电，检测到您的爱车车门尚未上锁，请留意哦
        配置项(存在hot_config表中，1-NIO_APP，2-SMS，3-VOICE，4-EMAIL):
        1. hermes.component.push.config 10min第一次推送的配置
            select value from hot_config where key='hermes.component.push.config'
            > [{'push_type':'2','platform_type':'1','compo':'doorlock'}]
        2. hermes.door.push.config 30min推送door状态电话的配置
            select value from hot_config where key='hermes.door.push.config'
            > [{'push_type':'3','platform_type':'1','compo':'doorlock'}]
        """
        door_status = {
            "door_locks": {
                "door_lock_frnt_le_sts": 0,  # 主驾车门未锁
                "door_lock_frnt_ri_sts": 1,
                "entry_meth": 3,
                "user_id": 9674,
                "access_mode": 20,
                "account_id": 2169565560
            },
            "door_ajars": {
                "door_ajar_frnt_le_sts": 1,
                "door_ajar_frnt_ri_sts": 1,
                "door_ajar_re_le_sts": 1,
                "door_ajar_re_ri_sts": 1
            },
            "charge_port_status": [
                {
                    "charge_port_sn": 1,
                    "ajar_status": 1
                },
                {
                    "charge_port_sn": 1,
                    "ajar_status": 1
                }
            ],
            "tailgate_status": {
                "ajar_status": 1
            },
            "engine_hood_status": {
                "ajar_status": 1
            },
            "vehicle_lock_status": 0
        }
        # 修改车辆状态满足前提条件
        # publish_msg_by_kafka('charge_end_event',
        #                      vehicle_status={'vehl_state': 2, 'comf_ena': 0, 'ntester': False},
        #                      sleep_time=2)
        # NT1上报大灯开启、车门未关、车门未锁
        publish_msg_by_kafka('light_change_event', light_status={'head_light_on': 1}, sleep_time=2, platform_type=0)
        publish_msg_by_kafka('door_change_event', door_status=door_status, sleep_time=2, platform_type=0)
        # publish_msg_by_kafka('door_change_event', door_status={'door_locks': {'door_lock_frnt_le_sts': 0}, 'vehicle_lock_status': 0}, sleep_time=2, platform_type=0)

        # 10分钟后查询kibana log关键字："vehicle component status push to app, vehicleId:{vid}, message:{msg}"
        # redis增加key: hermes_test:compo_push_last:9347f56bb63e4af190c1cfe744f8c45e ttl为3天，保证一个行程结束后三天内不会重复推送

        # NT2已绑定未激活的车上报大灯开启、车门未关、车门未锁
        vin = env['vehicles']['ET7_not_active']['vin']
        vid = env['vehicles']['ET7_not_active']['vehicle_id']
        publish_msg_by_kafka('light_change_event', vin=vin, vid=vid, light_status={'head_light_on': 1}, sleep_time=2, platform_type=1)
        publish_msg_by_kafka('door_change_event', vin=vin, vid=vid, door_status=door_status, sleep_time=2, platform_type=1)
        # publish_msg_by_kafka('door_change_event', vin=vin, vid=vid, door_status={'door_locks': {'door_lock_frnt_le_sts': 0}, 'vehicle_lock_status': 0}, sleep_time=2, platform_type=1)
        # 10分钟后查询kibana log关键字: push info error

        # NT2已激活的车上报大灯开启和车门未关、车门未锁
        vin = env['vehicles']['ET7_active']['vin']
        vid = env['vehicles']['ET7_active']['vehicle_id']
        publish_msg_by_kafka('light_change_event', vin=vin, vid=vid, light_status={'head_light_on': 1}, sleep_time=2, platform_type=1)
        publish_msg_by_kafka('door_change_event', vin=vin, vid=vid, door_status=door_status, sleep_time=2, platform_type=1)
        # publish_msg_by_kafka('door_change_event', vin=vin, vid=vid, door_status={'door_locks': {'door_lock_frnt_le_sts': 0}, 'vehicle_lock_status': 0}, sleep_time=2, platform_type=1)
        # 10min发短信，/acc/2/in/profile/query 接口查询语言、手机号, /api/2/in/message/cn/sms_push 接口发短信
        # redis增加key: hermes_test:compo_push_last:0e7f4cb1a1c94091adc30397e6fea4b2 ttl为3天，保证一个行程结束后三天内不会重复推送
        # 30min打电话 /acc/2/in/profile/query 接口查询语言、手机号, /api/2/in/message/cn/voice_message 接口打电话
        # redis增加key: hermes_test:compo_call_last:0e7f4cb1a1c94091adc30397e6fea4b2 ttl为3天，保证一个行程结束后三天内不会重复推送


    def test_journey_start_delete_redis(self, env, cmdopt, vid, redis, publish_msg_by_kafka):
        """
        journey_start_event 会将删除hermes_test:compo_push_last:vid
        """
        with allure.step("NT1"):
            # time.sleep(60)
            key1 = f"hermes_{cmdopt}:compo_push_last:{vid}"
            redis['cluster'].string_set(key1, "light")
            # 先报一条update事件，将时间戳写入本地缓存（本地缓存有效期1min）
            publish_msg_by_kafka('periodical_journey_update')
            publish_msg_by_kafka('journey_start_event')
            assert redis['cluster'].get(key1) is None

        with allure.step("NT2"):
            vin = env['vehicles']['ET7_active']['vin']
            vid = env['vehicles']['ET7_active']['vehicle_id']
            key2 = f"hermes_{cmdopt}:compo_push_last:{vid}"
            key3 = f"hermes_{cmdopt}:compo_call_last:{vid}"
            # redis['cluster'].string_set(key2, "light")
            # 先报一条update事件，将时间戳写入本地缓存（本地缓存有效期1min）
            publish_msg_by_kafka('periodical_journey_update', vin=vin, vid=vid)
            publish_msg_by_kafka('journey_start_event', vin=vin, vid=vid)
            assert redis['cluster'].get(key2) is None
            assert redis['cluster'].get(key3) is None
