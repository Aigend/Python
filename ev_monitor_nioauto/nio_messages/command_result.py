#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/06/30 23:18
@contact: hongzhen.bi@nio.com
@description: 生成command result

result_content填充的json示例：
    result_content = {
        "door_status": {
            "status": 0,
            "fail_reason": "fail_reason",
            "vehicle_status": {
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
                    "door_lock_frnt_le_sts": 1,
                    "door_lock_frnt_ri_sts": 1
                },
                "engine_hood_status": {
                    "ajar_status": 1
                },
                "tailgate_status": {
                    "ajar_status": 1
                },
                "vehicle_lock_status": 1
            }
        },
        "window_status": {
            "status": 0,
            "fail_reason": "fail_reason",
            "vehicle_status": {
                "sun_roof_positions": {
                    "sun_roof_posn": 65,
                    "sun_roof_posn_sts": 0,
                    "sun_roof_shade_posn": 63
                },
                "window_positions": {
                    "win_frnt_le_posn": 14,
                    "win_frnt_ri_posn": 85,
                    "win_re_le_posn": 87,
                    "win_re_ri_posn": 64
                }
            }
        },
        "heating_status": {
            "status_set_hvh": 0,
            "status_seats_heating": 0,
            "status_steering_wheel_heating": 0,
            "fail_reason_set_hvh": "fail_reason",
            "fail_reason_seats_heating": "fail_reason",
            "fail_reason_steering_wheel_heating": "fail_reason",
            "vehicle_status": {
                "steer_wheel_heat_sts": 0,
                "seat_heat_frnt_le_sts": 7,
                "seat_heat_frnt_ri_sts": 1,
                "seat_heat_re_le_sts": 2,
                "seat_heat_re_ri_sts": 1,
                "hv_batt_pre_sts": 1,
                "seat_vent_frnt_le_sts": 0,
                "seat_vent_frnt_ri_sts": 0
            }
        },
        "hvac_status": {
            "status": 0,
            "fail_reason": "fail_reason",
            "vehicle_status": {
                "air_con_on": True,
                "amb_temp_c": 76.5,
                "cbn_pre_sts": 1,
                "ccu_cbn_pre_ac_ena_sts": 0,
                "ccu_cbn_pre_aqs_ena_sts": 0,
                "outside_temp_c": 33,
                "pm_2p5_cabin": 110,
                "pm_2p5_filter_active": False
            }
        },
        "findme_status": {
            "status": 0,
            "fail_reason": "fail_reason",
        },
        "ac_plan_status": {
            "status": 0,
            "fail_reason": "fail_reason",
        }
    }
"""
import logging
from .utils.make_cmd_result_msg import make_generic_config_result_message, make_air_conditioner_cmdresult, make_doorlock_cmdresult, make_windows_sunroof_cmdresult_message, \
    make_tailgate_cmdresult, make_findme_cmdresult, make_ac_plan_cmdresult, make_air_purifier_cmdresult, get_rvs_upload_syslog, get_rvs_upload_adclog, make_default_result_message, make_nextev_message, \
    make_hvh_heating_cmdresult, make_seats_heating_cmdresult, make_steering_heating_cmdresult


def generate_message(command_content, result_content={}):
    command = {}
    for k, v in command_content['params'].items():
        if k == 'command_id':
            command[k] = int(v)
        else:
            command[k] = v

    command_name = 'command_result'
    if command_content['sub_type'] == 'rvs_generic_config':
        result_message = make_generic_config_result_message(command)
        command_name = 'config_result'
    elif command_content['sub_type'] == "rvs_set_air_conditioner":
        cmd_result = result_content.get('hvac_status', {})
        result_message = make_air_conditioner_cmdresult(command, cmd_result.get('status', 0), cmd_result.get('fail_reason', 'fail_reason'), cmd_result.get('vehicle_status', {}))
    elif command_content['sub_type'] == "rvs_set_doorlock":
        cmd_result = result_content.get('door_status', {})
        result_message = make_doorlock_cmdresult(command, cmd_result.get('status', 0), cmd_result.get('fail_reason', 'fail_reason'), cmd_result.get('vehicle_status', {}))
    elif command_content['sub_type'] == "rvs_set_windows_sunroof":
        cmd_result = result_content.get('window_status', {})
        result_message = make_windows_sunroof_cmdresult_message(command, cmd_result.get('status', 0), cmd_result.get('fail_reason', 'fail_reason'), cmd_result.get('vehicle_status', {}))
    elif command_content['sub_type'] == 'rvs_set_tailgate':
        cmd_result = result_content.get('door_status', {})
        result_message = make_tailgate_cmdresult(command, cmd_result.get('status', 0), cmd_result.get('fail_reason', 'fail_reason'), cmd_result.get('vehicle_status', {}))
    elif command_content['sub_type'] == 'rvs_exe_findme':
        cmd_result = result_content.get('findme_status', {})
        result_message = make_findme_cmdresult(command, cmd_result.get('status', 0), cmd_result.get('fail_reason', 'fail_reason'))
    elif command_content['sub_type'] == 'rvs_publish_ac_plan':
        cmd_result = result_content.get('ac_plan_status', {})
        result_message = make_ac_plan_cmdresult(command, cmd_result.get('status', 0), cmd_result.get('fail_reason', 'fail_reason'))
    elif command_content['sub_type'] == 'rvs_set_air_purifier':
        cmd_result = result_content.get('hvac_status', {})
        result_message = make_air_purifier_cmdresult(command, cmd_result.get('status', 0), cmd_result.get('fail_reason', 'fail_reason'), cmd_result.get('vehicle_status', {}))
    elif command_content['sub_type'] == 'rvs_set_hvh':
        cmd_result = result_content.get('heating_status', {})
        result_message = make_hvh_heating_cmdresult(command, cmd_result.get('status_set_hvh', 0), cmd_result.get('fail_reason_set_hvh', 'fail_reason'), cmd_result.get('vehicle_status', {}))
    elif command_content['sub_type'] == 'rvs_seats_heating':
        cmd_result = result_content.get('heating_status', {})
        result_message = make_seats_heating_cmdresult(command, cmd_result.get('status_seats_heating', 0), cmd_result.get('fail_reason_seats_heating', 'fail_reason'),
                                                      cmd_result.get('vehicle_status', {}))
    elif command_content['sub_type'] == 'rvs_steering_wheel_heating':
        cmd_result = result_content.get('heating_status', {})
        result_message = make_steering_heating_cmdresult(command, cmd_result.get('status_steering_wheel_heating', 0), cmd_result.get('fail_reason_steering_wheel_heating', 'fail_reason'),
                                                         cmd_result.get('vehicle_status', {}))
    # elif command_content['sub_type'] == 'rvs_trigger_instant_data':
    #     status, fail_reason, sleep, vehicle_status = set_cmd_param('make_instant_data_triger_cmdresult')
    #     result_message = make_instant_data_triger_cmdresult(command, status, fail_reason)
    # elif command_content['sub_type'] == 'rvs_set_guest_mode':
    #     status, fail_reason, sleep = set_cmd_param('make_instant_data_triger_cmdresult')
    #     result_message = make_instant_data_triger_cmdresult(command, status, fail_reason)
    elif command_content['sub_type'] == 'rvs_upload_syslog':
        result_message = get_rvs_upload_syslog(command)
    elif command_content['sub_type'] == 'rvs_upload_adcfiles':
        result_message = get_rvs_upload_adclog(command, result_content.get('file_path'))
    # elif command_content['sub_type'] == 'rvs_wlan_config':
    #     result_message = make_wlan_cmdresult(command)
    # elif command_content['sub_type'] == 'rvs_exe_dtc':
    # result_message = make_dtc_cmdresult(command)
    # elif command_content['sub_type'] == 'rvs_exe_dids':
    #     result_message = make_did_cmdresult(command)
    else:
        result_message = make_default_result_message(command)

    sub_type = command_content['sub_type']
    nextev_message = make_nextev_message("COMMAND_RESULT",
                                         sub_type,
                                         command_name,
                                         result_message)

    logging.info(f"----return nextevmsg----\n{nextev_message}")
    logging.info(f'----command_result----\n{result_message}')
    return nextev_message
