import time

from nio_messages.did import DIDS
# @pytest.mark.skip('Manual')


class TestPresetVehicleStatus(object):

    def test_preset_vehicle_status(self, publish_msg_by_kafka, mysql):
        """
        该方法为预置车辆初始状态

        """

        vid = 'acc29b798f47466d8db6d6d6af00807a'
        vehicle_data = mysql['rvs'].fetch('vehicle_profile', {"id": vid}, ['vin', 'model_type'])[0]
        vin = vehicle_data['vin']
        model_type = vehicle_data['model_type']

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
        window_status['sun_roof_positions']['sun_roof_posn'] = 101 if model_type.upper() in ['ES6', 'ET7', 'ET5'] else 0
        window_status['sun_roof_positions']['sun_roof_posn_sts'] = 4 if model_type.upper() == 'ES8' else 0

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

        publish_msg_by_kafka('instant_status_resp', vid=vid, vin=vin,
                             sample_point={
                                 "vehicle_status": vehicle_status,
                                 "position_status": position_status,
                                 "soc_status": soc_status,
                                 "door_status": door_status,
                                 "window_status": window_status,
                                 "hvac_status": hvac_status,
                                 "occupant_status": occupant_status
                             }, sleep_time=2)


    def test_did_update_msg(self, checker, publish_msg_by_kafka, mysql):
        vid = 'acc29b798f47466d8db6d6d6af00807a'
        vin = mysql['rvs'].fetch('vehicle_profile', {"id": vid}, ['vin'])[0]['vin']
        did_num=len(DIDS)
        # 构造并上报消息
        nextev_message, did_update_obj = publish_msg_by_kafka('did_update_event', did_data_num=did_num,vid=vid,vin=vin)


    def test_wti(self, publish_msg_by_kafka, checker,vid,vin):
        """
        """
        vid='acc29b798f47466d8db6d6d6af00807a'
        vin = 'SQETEST0235992417'
        signal_int = [
            # {'name': 'CooltLvlLowWarnReq', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-DI-2'},
            # {'name': 'EPFaultLevelWarning', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-EP-1'},
            {'name': 'ABSFailLampReq', 'value': 1, 'alarm_level': 1, 'evm_alarm_level': 2, 'alarm_code': 13, 'wti_code': 'WTI-BC-1'},
        ]
        nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': signal_int}, sleep_time=2,vid=vid,vin=vin)