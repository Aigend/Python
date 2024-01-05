#!/usr/bin/env python
# coding=utf-8

"""
详情：https://confluence.nevint.com/display/CVS/Specific+Events+Report

事件列表：
ac_plan_exec
        空调预约启动事件
        如果预约空调启动失败，RVS Server调用APP Msg（APP中台）接口api/1/in/app_msg/common 往APP push 信息。详情见test_ac_plan_exec.py

rain_wrm_event
        rvs_server转发special event上报的rain_wrm_event事件数据到kafka
        swc-cvs-tsp-test-80001-push_event (http://showdoc.nevint.com/index.php?s=/11&page_id=24395 )

        hermes监测到RainDetected之后，判断窗户和天窗状态，如果未关闭，向用户推送
        prd:https://confluence.nioint.com/pages/viewpage.action?pageId=276272698 

modem_event
        https://confluence.nioint.com/display/SEQ/Specific+Event
"""
import random
import string
import time

from nio_messages import pb2
from nio_messages.nextev_msg import gen_nextev_message


def generate_message(vin, vid, event_type, protobuf_v=pb2.VERSION, data=None, clear_fields=None):
    if not data:
        data = {}

    obj = {}
    obj['specific_event_type'] = event_type
    if event_type == 'power_swap_start':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['power_swap_id'] = data.get('power_swap_id', time.strftime("%Y%m%d", time.localtime()) + '0001')
        obj['soc'] = data.get('soc', random.randint(0, 200) * 0.5)
        obj['chg_subsys_encoding'] = data.get('chg_subsys_encoding', 'P0000084AH130YY0012340001YFTY49')
        # btry_cap字段没有上报
        # obj['btry_cap'] = data.get('btry_cap', round(random.uniform(0, 10000), 1))
        obj['dump_enrgy'] = data.get('dump_enrgy', round(random.uniform(0, 1000), 1))


    elif event_type == 'power_swap_end':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['power_swap_id'] = data.get('power_swap_id', time.strftime("%Y%m%d", time.localtime()) + '0001')
        obj['soc'] = data.get('soc', random.randint(0, 200) * 0.5)
        obj['chg_subsys_encoding'] = data.get('chg_subsys_encoding', 'P0000084AH130YY0012340001YFTY49')
        # btry_cap字段没有上报
        # obj['btry_cap'] = data.get('btry_cap', round(random.uniform(0, 10000), 1))
        obj['dump_enrgy'] = data.get('dump_enrgy', round(random.uniform(0, 1000), 1))

        obj['is_success'] = data.get('is_success', random.choice([True, False]))

    elif event_type == 'power_swap_failure':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['power_swap_id'] = str(int(time.time()))
        obj['failure_count'] = data.get('failure_count', str(random.randint(0, 10)))
        obj['fail_reason'] = data.get('fail_reason', "unknown1")
        obj['extend_info'] = data.get('extend_info', "others1")

    elif event_type == 'lv_batt_charging':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['lv_batt_soh_sul'] = data.get('lv_batt_soh_sul', random.randint(0, 100))
        obj['lv_batt_soh_lam'] = data.get('lv_batt_soh_lam', random.randint(0, 127))
        obj['lv_batt_soh_cor'] = data.get('lv_batt_soh_cor', round(random.uniform(0, 15), 1))
        obj['lv_batt_soh_sul_sts'] = data.get('lv_batt_soh_sul_sts', 1)
        obj['lv_batt_soh_lam_sts'] = data.get('lv_batt_soh_lam_sts', 1)
        obj['lv_batt_soh_cor_sts'] = data.get('lv_batt_soh_cor_sts', 1)
        obj['lv_batt_soc'] = data.get('lv_batt_soc', 1)
        obj['lv_batt_soc_sts'] = data.get('lv_batt_soc_sts', 1)
        obj['lv_batt_customer_id'] = data.get('lv_batt_customer_id', 1)
        obj['lv_batt_charging_event_id'] = data.get('lv_batt_charging_event_id', obj['sample_ts'])
        obj['lv_batt_charging_event_num'] = data.get('lv_batt_charging_event_num', random.choice([1, 2, 3, 4, 5]))
        obj['LVBattU'] = data.get('LVBattU', 0)
        obj['LVBattUSts'] = data.get('LVBattUSts', 0)
        obj['LVBattIRng'] = data.get('LVBattIRng', 0)
        obj['LVBattI'] = data.get('LVBattI', 0)
        obj['LVBattISts'] = data.get('LVBattISts', 0)
        obj['LVBattT'] = data.get('LVBattT', 0)
        obj['LVBattTSts'] = data.get('LVBattTSts', 0)
        obj['VCUHVBattCutOffWarn'] = data.get('VCUHVBattCutOffWarn', 0)
        obj['VCULvBattWarn'] = data.get('VCULvBattWarn', 0)
        obj['LVBattDchaWakeUpSts'] = data.get('LVBattDchaWakeUpSts', 0)
        obj['LVBattChrgWakeUpSts'] = data.get('LVBattChrgWakeUpSts', 0)
        obj['LVBattSOCWakeUpSts'] = data.get('LVBattSOCWakeUpSts', 0)
        obj['LVBattDchaWakeUp'] = data.get('LVBattDchaWakeUp', 0)
        obj['LVBattChrgWakeUp'] = data.get('LVBattChrgWakeUp', 0)
        obj['LVBattSOCWakeUp'] = data.get('LVBattSOCWakeUp', 0)
        obj['VCUHVDCDCMdReq'] = data.get('VCUHVDCDCMdReq', 0)
        obj['VCUReqOutputVoltg'] = data.get('VCUReqOutputVoltg', 0)
        obj['BCMVoltWakeupReq'] = data.get('BCMVoltWakeupReq', 0)
        obj['DCDCStatus'] = data.get('DCDCStatus', 0)
        obj['LVBattChgSts'] = data.get('LVBattChgSts', 0)
        obj['LoadShed'] = data.get('LoadShed', 0)
        obj['CGWVoltWakeupReq'] = data.get('CGWVoltWakeupReq', 0)
        obj['VehState'] = data.get('VehState', 0)
        obj['ComfEna'] = data.get('ComfEna', 0)
        obj['RemCtrlHVPwrMgnt'] = data.get('RemCtrlHVPwrMgnt', 0)
        obj['LVBattChrgReason'] = data.get('LVBattChrgReason', 0)
        obj['CGWLogVoltage'] = data.get('CGWLogVoltage', 0)
        obj['CGWLogSOC'] = data.get('CGWLogSOC', 0)
        if obj['lv_batt_charging_event_num'] == 1:
            obj['PreCGWLogInfo'] = data.get('PreCGWLogInfo', [{"sample_ts": obj['sample_ts'],
                                                               "CGWLogVoltage": round(random.uniform(220, 380), 1),
                                                               "CGWLogSOC": random.randint(0, 100)},
                                                              {"sample_ts": obj['sample_ts'],
                                                               "CGWLogVoltage": round(random.uniform(220, 380), 1),
                                                               "CGWLogSOC": random.randint(0, 100)
                                                               },
                                                              {"sample_ts": obj['sample_ts'],
                                                               "CGWLogVoltage": round(random.uniform(220, 380), 1),
                                                               "CGWLogSOC": random.randint(0, 100)
                                                               }])

    elif event_type == 'nfc_op':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['status'] = data.get('status', random.choice(["success", "fail"]))
        obj['action'] = data.get('action', "unlock_door")
        obj['aid'] = data.get('aid', random.choice(['f218c2dafbc110', 'f218c2dafbc120', 'f218c2dafbc130']))
        obj['device_id'] = data.get('device_id', 'sdfasdfsdfasdfsdfasdf')
        obj['user_id'] = data.get('user_id', 10090)
        obj['cert_serial_number'] = data.get('cert_serial_number', 'asdfasdfasfas')
        obj['ts_read_key'] = data.get('ts_read_key', int(round(time.time())))
        obj['ts_veri_key'] = data.get('ts_veri_key', int(round(time.time())))
        obj['key_id'] = data.get('key_id', time.strftime("%Y%m%d%H%M%s", time.localtime()))
        if obj['status'] == "success":
            obj['extend_info'] = data.get('extend_info', random.choice(['SuccessUnlockDoors', 'SuccessLockDoors']))
            obj['fail_reason'] = data.get('fail_reason', "")
        elif obj['status'] == "fail":
            obj['extend_info'] = data.get('extend_info', "")
            obj['fail_reason'] = data.get('fail_reason', random.choice(["nfc_device_error",
                                                                        "not_fresh_key",
                                                                        "private_key_mismatch",
                                                                        "aes_key_mismatch",
                                                                        "blacklist_key",
                                                                        "unstarted_key",
                                                                        "expired_key",
                                                                        "expired_virtualkey_cert",
                                                                        "vehicle_id_mismatch",
                                                                        "device_id_mismatch",
                                                                        "cert_snum_mismatch",
                                                                        "untrusted_cert",
                                                                        "virtualkey_sig_fail",
                                                                        "nfcsigner_sig_fail",
                                                                        "validate_key_fail"
                                                                        ]))
        else:
            raise Exception('nfc_op event type is wrong')

    elif event_type == 'nkc_nfc_op':
        obj['status'] = data.get('status', random.choice(["success", "fail"]))
        # action 0x01: unlock_entries, 0x02:lock_entries, 0x03: unlock_tailgate, 0x04: find_car, 0x05: immo, 0x06: lock_tailgate
        obj['action'] = data.get('action', random.choice(['1', '2', '3', '4', '5', '6']))
        obj['aid'] = data.get('aid', random.choice(['f218c2dafbc110', 'f218c2dafbc120', 'f218c2dafbc130']))
        obj['device_id'] = data.get('device_id', 'sdfasdfsdfasdfsdfasdf')
        obj['user_id'] = data.get('user_id', 10090)
        obj['cert_serial_number'] = data.get('cert_serial_number', 'asdfasdfasfas')
        obj['ts_read_key'] = data.get('ts_read_key', int(round(time.time())))
        obj['key_id'] = data.get('key_id', time.strftime("%Y%m%d%H%M%s", time.localtime()))
        obj['time_consuming'] = data.get('time_consuming', random.randint(1000, 3000))
        if obj['status'] == "success":
            obj['extend_info'] = data.get('extend_info', random.choice(['SuccessUnlockDoors', 'SuccessLockDoors']))
            obj['fail_reason'] = data.get('fail_reason', "")
        elif obj['status'] == "fail":
            obj['extend_info'] = data.get('extend_info', "")
            obj['fail_reason'] = data.get('fail_reason', random.choice(["nfc_device_error",
                                                                        "not_fresh_key",
                                                                        "private_key_mismatch",
                                                                        "aes_key_mismatch",
                                                                        "blacklist_key",
                                                                        "unstarted_key",
                                                                        "expired_key",
                                                                        "expired_virtualkey_cert",
                                                                        "vehicle_id_mismatch",
                                                                        "device_id_mismatch",
                                                                        "cert_snum_mismatch",
                                                                        "untrusted_cert",
                                                                        "virtualkey_sig_fail",
                                                                        "nfcsigner_sig_fail",
                                                                        "validate_key_fail"
                                                                        ]))
        else:
            raise Exception('nfc_op event type is wrong')

    elif event_type == 'power_home_auth_failure':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['fail_reason'] = data.get('fail_reason', "unknown")
        obj['extend_info'] = data.get('extend_info', "others")

    elif event_type == 'ac_plan_exec':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['status'] = data.get('status', random.choice(["success", "failure"]))
        obj['operation'] = data.get('operation', random.choice(["0", "1"]))
        if obj['status'] == "failure" and obj['operation'] == "1":
            obj['fail_reason'] = data.get('fail_reason',
                                          random.choice(['vehl_not_parked',
                                                         'seat_occp_frnt_le_exist',
                                                         'seat_occp_frnt_ri_exist',
                                                         'anti_theft_warn_on',
                                                         'comfort_enable_on',
                                                         'soc_low',
                                                         'door_frnt_le_open',
                                                         'door_frnt_ri_open',
                                                         'door_re_le_open',
                                                         'door_re_ri_open',
                                                         'tailgate_open',
                                                         'invalid',
                                                         'Remote Cabin Control Stop',
                                                         'turn_on_malf']))
        elif obj['status'] == "failure" and obj['operation'] == "0":
            obj['fail_reason'] = data.get('fail_reason',
                                          random.choice(['vehl_not_parked',
                                                         'seat_occp_frnt_le_exist',
                                                         'seat_occp_frnt_ri_exist',
                                                         'anti_theft_warn_on',
                                                         'comfort_enable_on',
                                                         'soc_low',
                                                         'door_frnt_le_open',
                                                         'door_frnt_ri_open',
                                                         'door_re_le_open',
                                                         'door_re_ri_open',
                                                         'tailgate_open',
                                                         'invalid',
                                                         'turn_off_malf']))
        elif obj['status'] == "success":
            obj['fail_reason'] = ""
        else:
            raise Exception('ac_plan_exec event is wrong')
        obj['plan_id'] = data.get('plan_id', "10001-1501234567010")
        obj['amb_temp_c'] = data.get('amb_temp_c', round(random.uniform(10, 40), 1))
        obj['outside_temp_c'] = data.get('outside_temp_c', round(random.uniform(-20, 40), 1))
        obj['soc'] = data.get('soc', random.randint(0, 200) * 0.5)
        obj['target_temperature'] = data.get('target_temperature', round(random.uniform(20, 30), 1))

    elif event_type == 'hv_battery_pre_heating':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['HVBattPreSts'] = data.get('HVBattPreSts', 1)
        obj['HVBattPreEstimdTi'] = data.get('HVBattPreEstimdTi', 1)
        obj['calculate_heating_fail'] = data.get('calculate_heating_fail', "failure")
        obj['start_heating_fail'] = data.get('start_heating_fail', "failure")
        obj['stop_heating_fail'] = data.get('stop_heating_fail', "failure")
        if "failure" in (obj['calculate_heating_fail'], obj['start_heating_fail'], obj['stop_heating_fail']):
            obj['reason'] = data.get('reason', "others")
        else:
            raise Exception('hv_battery_pre_heating event is wrong')

    elif event_type == 'gd_alert_can_rate':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['alert_ts'] = data.get('alert_ts', int(round(time.time() * 1000)) - 10000)
        obj['monitor_window'] = data.get('monitor_window', 60)
        obj['events'] = data.get('events', [{"can_id": random.randint(100, 200),
                                             "type": 0,
                                             "severity": random.randint(1, 5),
                                             "detected_events": random.randint(1, 10),
                                             "actual_frames": random.randint(100, 300),
                                             "expected_frames": random.randint(50, 200)
                                             },
                                            {"can_id": random.randint(100, 200),
                                             "type": 0,
                                             "severity": random.randint(1, 5),
                                             "detected_events": random.randint(1, 10),
                                             "actual_frames": random.randint(100, 300),
                                             "expected_frames": random.randint(50, 200)
                                             }])

    elif event_type == 'deep_sleep':
        obj['type'] = data.get('type', random.choice([1, 2]))
        obj['soc'] = data.get('soc', random.randint(0, 200) * 0.5)
        obj['VehSleepSts'] = data.get('VehSleepSts', random.choice([0, 1, 2, 3, 4, 15]))
        obj['LVbattSOCSts'] = data.get('LVbattSOCSts', random.randint(0, 3))
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['event_id'] = data.get('event_id', int(round(time.time() * 1000)))

    elif event_type == 'fod_conf':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['command_id'] = data.get('command_id', "123456789")
        obj['status'] = data.get('status', 0)
        obj['fail_reason'] = data.get('fail_reason', "unknown")

    elif event_type == 'toby_event':
        # "toby_event Toby升级的事件，4g模块的固件"
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['event_type'] = data.get('event_type', random.choice(
            ['sw_error', 'sw_reset', 'hw_error', 'emergency_switch_off', 'toby_dead']))
        obj['event_detail'] = data.get('event_detail', "CMIOT check fails")

    elif event_type == 'fota_trigger_event':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['ecu'] = data.get('ecu', "CGW")
        obj['name'] = data.get('name', "fota_start_ack")

    elif event_type == 'fota_state_notify':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['state'] = data.get('state', int(round(time.time() * 1000)))
        obj['state_str'] = data.get('state_str', "unknown")

    elif event_type == 'rain_wrm_event':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['event_detail'] = data.get('event_detail', random.choice(['Normal', 'RainDetected', 'RainSensorFailure']))

    elif event_type == 'max_charging_soc_event':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000) - 600000))
        obj['set_max_soc_value'] = data.get('set_max_soc_value', random.randint(160, 200) * 0.5)
        obj['current_max_soc_value'] = data.get('current_max_soc_value', random.randint(160, 200) * 0.5)

    elif event_type == 'bms_dtc_info':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['result'] = data.get('result', random.choice(['success', 'fail']))
        if obj['result'] == 'fail':
            obj['nrc'] = data.get('nrc', 0x11)
        if obj['result'] == 'success':
            obj['dtc_list'] = data.get('dtc_list', [{"dtc": "d98687", "status": "0x2f"},
                                                    {"dtc": "978113", "status": "0x2f"},
                                                    {"dtc": "97d012", "status": "0x2f"}])
    elif event_type == 'modem_event':
        """
        modem_event业务逻辑参考：https://confluence.nioint.com/display/SEQ/Specific+Event
        
        """
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['module_type'] = data.get('module_type',
                                      random.choice(['toby', 'quectel']))  # 是两个4G模块， 现在用的toby，后面会用quectel
        obj['event_type'] = data.get('event_type', "disconnect")  # 目前只有disconnect

        ts = int(round(time.time() * 1000))

        event_detail = {
            "start": {"sample_ts": ts - 10 * 60 * 1000,  # required
                      "vehicle_state": 0,  # required, same with the VehicleState in proto
                      "process_id": ""  # optional, if vehicle_state is  parked, it is not needed
                      },
            "end": {"sample_ts": ts,
                    "vehicle_state": 0,
                    "process_id": ""
                    },
            "reason": 1,
            # required, 1--at freeze, 2--crash, 3--soft failure, 4–hard failure, 5–socket failure, 255 --other
            "restore_reason": {  # optional
                "soft_reset": 1,
                "graceful_reset": 1,
                "hard_reset": 1,
                "emergency_switch_off": 1
            }
        }

        obj['event_detail'] = data.get('event_detail', event_detail)

    elif event_type == 'ble_op_event':
        # obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        status = data.get('status', random.choice(['success', 'fail']))
        obj["status"] = status  # either one of {success, fail}
        obj["aid"] = data.get('aid', random.choice(['A000000809434343444B46E020', 'A000000809434343444B46E010',
                                                    '']))  # either one of ' A000000809434343444B46E020'  ' A000000809434343444B46E010' or empty
        obj["action"] = data.get('action', random.choice([0, 1, 2, 3, 4, 5,
                                                          6]))  # either one of {0x00: authentication, 0x01: unlock_entries, 0x02:lock_entries, 0x03: unlock_tailgate, 0x04: find_car, 0x05: immo, 0x06: lock_tailgate}
        obj["action_mode"] = data.get('action_mode',
                                      random.choice(['active', 'passive']))  # either one of 'active' 'passive'
        obj["conn_start_ts"] = data.get('conn_start_ts',
                                        int(time.time() * 1000))  # the timestamp (millisecond) of beginning to establish a connection
        obj["conn_end_ts"] = data.get('conn_end_ts',
                                      int(time.time() * 1000))  # the timestamp (millisecond) of breaking up a connection
        obj["read_ts"] = data.get('read_ts',
                                  int(time.time() * 1000))  # the timestamp (millisecond) of reading key or triggering the action.
        obj["verify_ts"] = data.get('verify_ts',
                                    int(time.time() * 1000))  # the timestamp (millisecond) of verifying key or ending the action.
        obj["s_random"] = data.get('s_random', ''.join(random.sample(string.ascii_letters + string.digits,
                                                                     16)))  # the random value which kept during the whole session
        obj["realtime_cipher_pre"] = data.get('realtime_cipher_pre', ''.join(
            random.sample(string.ascii_letters + string.digits, 6)))  # the first six letters of the realtime_cipher
        obj["device_id"] = data.get('device_id', ''.join(
            random.sample(string.ascii_letters, 32)))  # required, device_id of the virtual key
        obj["vehicle_id"] = data.get('vehicle_id', vid)  # required, vehicle id
        obj["device_rssi"] = data.get('device_rssi', random.randint(0, 100))  # RSSI received from device
        obj["vehicle_rssi"] = data.get('vehicle_rssi', random.randint(0, 100))  # RSSI monitored by the Vehicle BTM/CGW
        obj["action_latency"] = data.get('action_latency', random.randint(0,
                                                                          3000))  # latency from CGW/BGW from accepting ACTION to action done, millisecond
        if status == "success":
            obj["fail_reason"] = ""
            obj["key_id"] = data.get('key_id', ''.join(
                random.sample(string.ascii_letters + string.digits, 16)))  # required if status = 'success'
            obj["user_id"] = data.get('user_id', random.randint(100000,
                                                                1020000000))  # required if status = 'success', string type to adapt to CGW
        else:
            obj["fail_reason"] = data.get('fail_reason', "dk_cert_verify_failed")
            obj["key_id"] = ""
            obj["user_id"] = ""

    elif event_type == 'ventilation_dry_event':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['event_type'] = data.get('event_type', "instant")  # 目前只有disconnect
        obj['event_detail'] = data.get('event_detail', "timeout")

    elif event_type == "car_key_settings_event":
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj["set_pas_key_switch_sts"] = data.get('set_pas_key_switch_sts',
                                                 random.choice(["on", "off"]))  # optional, which is from TSP
        obj["current_pas_key_switch_sts"] = data.get('current_pas_key_switch_sts', random.choice(
            ["on", "off"]))  # required, which is the current status, either 'on' or 'off'
        obj["media_type"] = data.get('media_type', random.choice(["ble", "lfrf"]))  # such as 'ble' 'lfrf'

    elif event_type == 'cdc_pin2_immo_event':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj["event_type"] = data.get('event_type', random.choice(["enable", "disable", "unlock"]))
        obj["user_id"] = data.get('user_id', '402355066')
        obj["event_detail"] = data.get('event_detail', random.choice(['cdc_pin2_immo_enable', 'cdc_pin2_immo_disable',
                                                                      'cdc_pin2_immo_unlock',
                                                                      'cdc_pin2_immo_no_left_times']))
    elif event_type == 'fota_package_download_switch':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj["switch_sts"] = data.get('switch_sts', random.choice(["on", "off"]))

    elif event_type == 'ble_apu_wal_event':
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj['vehicle_id'] = vid
        obj['device_type'] = data.get('device_type', random.choice([0x0A, 0xA1, 0xA2]))
        obj['trigger_reason'] = data.get('trigger_reason', random.choice(['no_unlock_trig_on_enter_unlock_zone',
                                                                          'no_lock_trig_on_all_leave_lock_zone',
                                                                          'no_wlc_trig_on_enter_wlc_zone',
                                                                          'any_lock_trigger',
                                                                          'vehl_sts_to_dp']))
        obj['device_address'] = data.get('device_address', random.choice(['112233445566', '112233445566112233445566']))
        obj['signal'] = data.get('signal', [{'k':'ApuFlagDevX', 'v': random.randint(0, 5)},
                                            {'k':'ApuTraceDetd', 'v': random.randint(0, 1)},
                                            {"k": "BTA5_UWB", "v": random.randint(0, 4095)},
                                            {"k": "SmtKey_PosnModeDev1", "v": random.randint(0, 6)},
                                            {"k": "KeyFobBattVolt", "v": 0},
                                            {"k": "ImmoDevInFlag", "v": random.randint(0, 1)},
                                            {"k": "AntiLockFlag", "v": random.randint(0, 1)},
                                            {"k": "CenLockReq", "v": random.randint(0, 13)}])

    elif event_type in ['air_conditioner_event', 'steer_wheel_heating_event', 'seat_heating_event', 'seat_ventilation_event']:
        obj['sample_ts'] = data.get('sample_ts', int(round(time.time() * 1000)))
        obj["event_type"] = data.get('event_type', random.choice(["instant", "schedule"]))
        details = ['vehl_not_parked', 'comfort_enable_on', 'soc_low', 'oncar_system_error']
        if event_type != 'air_conditioner_event':
            details.append('dcdc_status_not_working')
        obj["event_detail"] = data.get('event_detail', random.choice(details))

    else:
        raise Exception('event_type {} is wrong'.format(event_type))

    if clear_fields:
        for item in clear_fields:
            del (obj[item])

    nextev_msg = gen_nextev_message('rvs_events_report',
                                    data=obj,
                                    publish_ts=obj.get('sample_ts', int(round(time.time() * 1000))),
                                    version=protobuf_v,
                                    account_id=vid
                                    )

    return nextev_msg, obj
