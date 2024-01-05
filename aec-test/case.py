"""
@Author: wenlong.jin
@File: case.py
@Project: aec-test
@Time: 2023/7/13 14:59
"""
import json
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from algorith import *
from concurrent.futures import ThreadPoolExecutor, as_completed


def Test_Single_Algorith_001(lock, pub_socket, data, detail, params):
    """
    触发BBSA算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        open_param = {"step": "1001",
                      "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
                      "params": json.dumps({"battery_type": "1", "station_type": "2", })}
        message = {"command": "AEC-BBSA", "result": {}, "delay": 10}
        close_param = {"step": "1002", "service_id": "", }
        result = open_bbsa_1001(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_bbsa_1002(lock, pub_socket, data, close_param)
        message["result"] = result
        sync_check_algorith_stop_result(data, detail, message)
    else:
        open_param = {"step": "1001",
                      "service_id": "PS-NIO-31da205c-64ba4b36d5e877336b7642d18dec0ce598dd34d81690789489607",
                      "params": json.dumps(
                          {"vehicle_type": "ES8",
                           "battery_type": "70",
                           "is_unmanned_station": "1",
                           "station_type": "1",
                           "locate_stage": "2"})}
        message = {"command": "BBSA", "result": {}, "delay": 10}
        close_param = {"step": "1002", "service_id": "", }
        result = open_bbsa_1001(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_bbsa_1002(lock, pub_socket, data, close_param)
        # message["result"] = result
        # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_002(lock, pub_socket, data, detail, params):
    """
    触发BSA算法，并收集对仿真照片的结果
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        open_param = {"step": "1101",
                      "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
                      "params": json.dumps({"battery_type": "2",
                                            "station_type": "2",
                                            "battery_bms_pack_id": "P0079340AP33620006130X001A00015"
                                            })}
        message = {"command": "AEC-BSA", "result": {}, "delay": 10}
        close_param = {"step": "1102", "service_id": "", }
        result = open_bsa_1101(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_bsa_1102(lock, pub_socket, data, close_param)
        message["result"] = result
        sync_check_algorith_stop_result(data, detail, message)
    else:
        open_param = {"step": "1101",
                      "service_id": "PS-NIO-31da205c-64ba4b36d5e877336b7642d18dec0ce598dd34d81690789489607",
                      "params": json.dumps(
                          {"vehicle_type": "ES8",
                           "battery_type": "70",
                           "is_unmanned_station": "1",
                           "station_type": "1",
                           "locate_stage": "1",
                           "battery_bms_pack_id": "P0296681AB34322V8788683JA000005"})}
        message = {"command": "BATTERY-UP-SURFACE-CHECK", "result": {}, "delay": 10}
        close_param = {"step": "1102", "service_id": "", }
        result = open_bsa_1101(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_bsa_1102(lock, pub_socket, data, close_param)
        # message["result"] = result
        # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_003(lock, pub_socket, data, detail, params):
    """
    触发BSCC算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = params.get("version", 2)
    if version == 2:
        open_param = {"step": "1201",
                      "service_id": "PS-NIO-31da205c-64ba4b364b220be3d04547a904788454400010201691044527111",
                      "params": json.dumps({
                          "vehicle_type": "NT2-ES8",
                          "battery_type": "100",
                          "is_unmanned_station": "1",
                          "station_type": "1",
                          "locate_stage": "1",
                          "battery_bms_pack_id": "P0205908AJ32921V218952L13B00308"}
                      )}
        message = {"command": "BATTERY-SURFACE-CAMERA-CHECK", "result": {}, "delay": 10}
        close_param = {"step": "1202", "service_id": "", }
    else:
        msg = f"params not get correct version:{version}, not support"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)
        return
    result = open_bscc_1201(lock, pub_socket, data, open_param)
    message["result"] = result
    sync_check_algorith_result(data, detail, message)
    time.sleep(5)
    result = close_bscc_1202(lock, pub_socket, data, close_param)
    # message["result"] = result
    # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_004(lock, pub_socket, data, detail, params):
    """
    触发PiP算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        open_param = {"step": "1301", "service_id": "",
                      "params": json.dumps({"vehicle_type": "ES6",
                                            "is_unmanned_station": "1",
                                            "station_type": "2"})}
        message = {"command": "AEC-PiP", "result": {}, "delay": 10}
        close_param = {"step": "1302", "service_id": "", }
        result = open_pip_1301(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_pip_1302(lock, pub_socket, data, close_param)
        message["result"] = result
        sync_check_algorith_stop_result(data, detail, message)
    else:
        open_param = {"step": "1301", "service_id": "",
                      "params": json.dumps({"vehicle_type": "ES8",
                                            "battery_type": "",
                                            "is_unmanned_station": "1",
                                            "station_type": "1"})}
        message = {"command": "HUMAN-ACTIVITY", "result": {}, "delay": 10}
        close_param = {"step": "1302", "service_id": "", }
        result = open_pip_1301(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_pip_1302(lock, pub_socket, data, close_param)
        # message["result"] = result
        # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_005(lock, pub_socket, data, detail, params):
    """
    触发PPP算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        open_param = {"step": "1401", "service_id": "", "params": json.dumps({"station_type": "2"})}
        message = {"command": "AEC-PPP", "result": {}, "delay": 4}
        close_param = {"step": "1402", "service_id": "", }
        result = open_ppp_1401(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        time.sleep(random.randint(2, 6))
        result = close_ppp_1402(lock, pub_socket, data, close_param)
        message["result"] = result
        sync_check_algorith_stop_result(data, detail, message)
    else:
        open_param = {"step": "1401", "service_id": "", "params": json.dumps({"station_type": "1"})}
        message = {"command": "PARKING-HUMAN-DETECTION", "result": {}, "delay": 4}
        close_param = {"step": "1402", "service_id": "", }
        result = open_ppp_1401(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        time.sleep(random.randint(2, 6))
        result = close_ppp_1402(lock, pub_socket, data, close_param)
        # message["result"] = result
        # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_006(lock, pub_socket, data, detail, params):
    """
    触发RSDV_PiP算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        open_param = {"step": "1301", "service_id": "",
                      "params": json.dumps({"vehicle_type": "ES6",
                                            "is_unmanned_station": "1",
                                            "station_type": "2"})}
        message = {"command": "AEC-PiP", "result": {}, "delay": 10}
        close_param = {"step": "1302", "service_id": "", }
        result = open_pip_1301(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_pip_1302(lock, pub_socket, data, close_param)
        message["result"] = result
        sync_check_algorith_stop_result(data, detail, message)
    else:
        open_param = {"step": "1501",
                      "service_id": "PS-NIO-31da205c-64ba4b364b220be3d04547a904788454400010201691045157093",
                      "params": json.dumps({"vehicle_type": "NT2-ES8",
                                            "station_type": "1"})}
        message = {"command": "RSDV_PiP", "result": {}, "delay": 10}
        close_param = {"step": "1502", "service_id": "", }
        result = open_rsdv_pip_1501(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_rsdv_pip_1502(lock, pub_socket, data, close_param)
        # message["result"] = result
        # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_007(lock, pub_socket, data, detail, params):
    """
    触发RSDV_VLSV2算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = params.get("version", 2)
    if version == 2:
        open_param = {"step": "1601",
                      "service_id": "PS-NIO-31da205c-64ba4b364b220be3d04547a904788454400010201691045157093",
                      "params": json.dumps({"vehicle_type": "NT2-ES8", "station_type": "1", })}
        message = {"command": "RSDV_VLSV2", "result": {}, "delay": 10}
        close_param = {"step": "1602", "service_id": "", }
    else:
        msg = f"params not get correct version:{version}, not support"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)
        return
    result = open_rsdv_vlsv2_1601(lock, pub_socket, data, open_param)
    message["result"] = result
    sync_check_algorith_result(data, detail, message)
    result = close_rsdv_vlsv2_1602(lock, pub_socket, data, close_param)
    # message["result"] = result
    # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_008(lock, pub_socket, data, detail, params):
    """
    触发SMD算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = params.get("version", 2)
    if version == 2:
        open_param = {"step": "1701",
                      "service_id": "PS-NIO-31da205c-64ba4b364b220be3d04547a904788454400010201691048607684",
                      "params": json.dumps({
                          "vehicle_type": "NT2-ES8",
                          "battery_type": "70",
                          "filter": {
                              "id": ["6", "7", "8", "3", "4", "5"],
                              "count": "1",
                              "lower": "0.2",
                              "upper": "1.0",
                              "threshold": "0.8"},
                          "is_unmanned_station": "1",
                          "station_type": "1",
                          "locate_stage": "1"})}
        message = {"command": "SCREW-SOCKET-MISSING", "result": {}, "delay": 10}
        close_param = {"step": "1702", "service_id": "", }
    else:
        msg = f"params not get correct version:{version}, not support"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)
        return
    result = open_smd_1701(lock, pub_socket, data, open_param)
    message["result"] = result
    sync_check_algorith_result(data, detail, message)
    result = close_smd_1702(lock, pub_socket, data, close_param)
    # message["result"] = result
    # sync_check_algorith_stop_result(data, detail, message)


# def Test_Single_Algorith_009(lock, pub_socket, data, detail, params):
#     """
#     触发VASF算法，并收集对仿真照片的结果
#     :param lock:
#     :param pub_socket:
#     :param data:
#     :param detail:
#     :param params:
#     :return:
#     """
#     pass
#     version = int(params.get("version", 3))
#     if version == 3:
#         open_param = {"step": "1001",
#                       "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
#                       "params": json.dumps({"battery_type": "1", "station_type": "2", })}
#         message = {"command": "AEC-BBSA", "result": {}, "delay": 10}
#         close_param = {"step": "1002", "service_id": "", }
#     else:
#         msg = f"params not get correct version:{version}, not support"
#         log.error(msg)
#         data["result"] = "FAIL"
#         data["data"].append(msg)
#         return
#     result = open_bbsa_1001(lock, pub_socket, data, open_param)
#     message["result"] = result


# def Test_Single_Algorith_010(lock, pub_socket, data, detail, params):
#     """
#     触发VBCC算法，并收集对仿真照片的结果
#     :param lock:
#     :param pub_socket:
#     :param data:
#     :param detail:
#     :param params:
#     :return:
#     """
#     pass
#     version = int(params.get("version", 3))
#     if version == 3:
#         open_param = {"step": "1001",
#                       "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
#                       "params": json.dumps({"battery_type": "1", "station_type": "2", })}
#         message = {"command": "AEC-BBSA", "result": {}, "delay": 10}
#         close_param = {"step": "1002", "service_id": "", }
#     else:
#         msg = f"params not get correct version:{version}, not support"
#         log.error(msg)
#         data["result"] = "FAIL"
#         data["data"].append(msg)
#         return
#     result = open_bbsa_1001(lock, pub_socket, data, open_param)
#     message["result"] = result


# def Test_Single_Algorith_011(lock, pub_socket, data, detail, params):
#     """
#     触发VBSL算法，并收集对仿真照片的结果
#     :param lock:
#     :param pub_socket:
#     :param data:
#     :param detail:
#     :param params:
#     :return:
#     """
#     pass
#     version = int(params.get("version", 3))
#     if version == 3:
#         open_param = {"step": "1001",
#                       "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
#                       "params": json.dumps({"battery_type": "1", "station_type": "2", })}
#         message = {"command": "AEC-BBSA", "result": {}, "delay": 10}
#         close_param = {"step": "1002", "service_id": "", }
#     else:
#         msg = f"params not get correct version:{version}, not support"
#         log.error(msg)
#         data["result"] = "FAIL"
#         data["data"].append(msg)
#         return
#     result = open_bbsa_1001(lock, pub_socket, data, open_param)
#     message["result"] = result


# def Test_Single_Algorith_012(lock, pub_socket, data, detail, params):
#     """
#     触发ViP算法，并收集对仿真照片的结果
#     :param lock:
#     :param pub_socket:
#     :param data:
#     :param detail:
#     :param params:
#     :return:
#     """
#     pass
#     version = int(params.get("version", 3))
#     if version == 3:
#         open_param = {"step": "1001",
#                       "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
#                       "params": json.dumps({"battery_type": "1", "station_type": "2", })}
#         message = {"command": "AEC-BBSA", "result": {}, "delay": 10}
#         close_param = {"step": "1002", "service_id": "", }
#     else:
#         msg = f"params not get correct version:{version}, not support"
#         log.error(msg)
#         data["result"] = "FAIL"
#         data["data"].append(msg)
#         return
#     result = open_bbsa_1001(lock, pub_socket, data, open_param)
#     message["result"] = result


def Test_Single_Algorith_013(lock, pub_socket, data, detail, params):
    """
    触发ViP2算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        open_param = {"step": "2201", "service_id": "", "params": json.dumps({"is_rsdv": "0"})}
        message = {"command": "AEC-ViP", "result": {}, "delay": 15}
        close_param = {"step": "2202", "service_id": "", }
        result = open_vip2_2201(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_vip2_2202(lock, pub_socket, data, close_param)
        message["result"] = result
        sync_check_algorith_stop_result(data, detail, message)
    else:
        open_param = {"step": "2201", "service_id": "2", "params": ""}
        message = {"command": "CAR-IN-PLATFORM", "result": {}, "delay": 15}
        close_param = {"step": "2202", "service_id": "", }
        result = open_vip2_2201(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_vip2_2202(lock, pub_socket, data, close_param)
        # message["result"] = result
        # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_014(lock, pub_socket, data, detail, params):
    """

    :param pub_socket:
    :param data:
    :param detail:
    :return:
    """
    version = params.get("version", 2)
    if version == 2:
        open_param = {"step": "2301",
                      "service_id": "",
                      "params": json.dumps({"vehicle_type": "", "station_type": "1", })}
        message = {"command": "VOR", "result": {}, "delay": 10}
        close_param = {"step": "2302", "service_id": "", }
    else:
        msg = f"params not get correct version:{version}, not support"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)
        return
    result = open_vor_2301(lock, pub_socket, data, open_param)
    message["result"] = result
    sync_check_algorith_result(data, detail, message)
    result = close_vor_2302(lock, pub_socket, data, close_param)
    # message["result"] = result
    # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_015(lock, pub_socket, data, detail, params):
    """
    触发WL算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        open_param = {"step": "2401", "service_id": "", "params": json.dumps({"auth_step": "1"})}
        message = {"command": "AEC-WL", "result": {}, "delay": 10}
        close_param = {"step": "2402", "service_id": "", }
        result = open_wl_2401(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        time.sleep(random.randint(2, 4))
        result = close_wl_2402(lock, pub_socket, data, close_param)
        message["result"] = result
        sync_check_algorith_stop_result(data, detail, message)
    else:
        open_param = {"step": "2401",
                      "service_id": "PS-NIO-31da205c-64ba4b364b220be3d04547a904788454400010201691044527111",
                      "params": json.dumps({"vehicle_type": "1", "auth_step": "2"})}
        message = {"command": "WHEEL-LOCATE", "result": {}, "delay": 10}
        close_param = {"step": "2402", "service_id": "", }
        result = open_wl_2401(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        time.sleep(random.randint(2, 4))
        result = close_wl_2402(lock, pub_socket, data, close_param)
        # message["result"] = result
        # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_016(lock, pub_socket, data, detail, params):
    """
    触发WLCC算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    pass
    version = params.get("version", 2)
    if version == 2:
        open_param = {"step": "2501",
                      "service_id": "PS-NIO-31da205c-64ba4b364b220be3d04547a904788454400010201691044527111",
                      "params": json.dumps({"vehicle_type": "NT2-ES8", "station_type": "1", })}
        message = {"command": "WHEEL-LOCATE-CAMERA-CHECK", "result": {}, "delay": 10}
        close_param = {"step": "2502", "service_id": "", }
    else:
        msg = f"params not get correct version:{version}, not support"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)
        return
    result = open_wlcc_2501(lock, pub_socket, data, open_param)
    message["result"] = result
    sync_check_algorith_result(data, detail, message)
    result = close_wlcc_2502(lock, pub_socket, data, close_param)
    # message["result"] = result
    # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_017(lock, pub_socket, data, detail, params):
    """
    触发RSDS算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        open_param_1 = {"step": "2601", "service_id": "", "params": json.dumps({})}
        open_param_2 = {"step": "2601", "service_id": "", "params": json.dumps({"door_action": "1"})}
        message = {"command": "AEC-RSDS", "result": {}, "delay": 15}
        close_param = {"step": "2602", "service_id": "", }
        open_rsds_2601(lock, pub_socket, data, open_param_1)
        time.sleep(random.randint(1, 2))
        result = open_rsds_2601(lock, pub_socket, data, open_param_2)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_rsds_2602(lock, pub_socket, data, close_param)
        message["result"] = result
        sync_check_algorith_stop_result(data, detail, message)
    else:
        open_param = {"step": "2601",
                      "service_id": "PS-NIO-31da205c-64ba4b364b220be3d04547a904788454400010201691045157093",
                      "params": json.dumps({"vehicle_type": "NT2-ES8", "station_type": "1"})}
        message = {"command": "RSDS", "result": {}, "delay": 15}
        close_param = {"step": "2602", "service_id": "", }
        result = open_rsds_2601(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_rsds_2602(lock, pub_socket, data, close_param)
        # message["result"] = result
        # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_018(lock, pub_socket, data, detail, params):
    """
    触发SAPA算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = params.get("version", 2)
    if version == 2:
        open_param = {"step": "2701",
                      "service_id": "PS-NIO-31da205c-64ba4b364b220be3d04547a904788454400010201691048607684",
                      "params": json.dumps({
                          "station_type": "1",
                          "is_unmanned_station": "1",
                          "park_direction": "1"})}
        message = {"command": "SAPA", "result": {}, "delay": 10}
        close_param = {"step": "2702", "service_id": "", }
    else:
        msg = f"params not get correct version:{version}, not support"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)
        return
    result = open_sapa_2701(lock, pub_socket, data, open_param)
    message["result"] = result
    sync_check_algorith_result(data, detail, message)
    result = close_sapa_2702(lock, pub_socket, data, close_param)
    # message["result"] = result
    # sync_check_algorith_stop_result(data, detail, message)


def Test_Single_Algorith_019(lock, pub_socket, data, detail, params):
    """
    触发BBCC算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = params.get("version", 2)
    if version == 2:
        open_param = {"step": "2801",
                      "service_id": "PS-NIO-31da205c-64ba4b364b220be3d04547a904788454400010201691044527111",
                      "params": json.dumps({
                          "vehicle_type": "NT2-ES8",
                          "battery_type": "70",
                          "filter": {
                              "id": ["6", "7", "8", "3", "4", "5"],
                              "count": "1",
                              "lower": "0.2",
                              "upper": "1.0",
                              "threshold": "0.8"},
                          "is_unmanned_station": "1",
                          "station_type": "1",
                          "locate_stage": "1"})}
        message = {"command": "BBCC", "result": {}, "delay": 10}
        close_param = {"step": "2802", "service_id": "", }
    else:
        msg = f"params not get correct version:{version}, not support"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)
        return
    result = open_bbcc_2801(lock, pub_socket, data, open_param)
    message["result"] = result
    # sync_check_algorith_result(data, detail, message)
    result = close_bbcc_2802(lock, pub_socket, data, close_param)


def Test_Single_Algorith_020(lock, pub_socket, data, detail, params):
    """
    触发WPV算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        open_param = {"step": "2901", "service_id": "", "params": ""}
        message = {"command": "AEC-WPV", "result": {}, "delay": 10}
        close_param = {"step": "2902", "service_id": "", }
        result = open_wpv_2901(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_wpv_2902(lock, pub_socket, data, close_param)
        message["result"] = result
        sync_check_algorith_stop_result(data, detail, message)
    else:
        open_param = {"step": "2901",
                      "service_id": "PS-NIO-31da205c-64ba4b364b220be3d04547a904788454400010201691044527111",
                      "params": json.dumps({
                          "station_type": "1",
                          "vehicle_type": ""
                      })}
        message = {"command": "WPV", "result": {}, "delay": 10}
        close_param = {"step": "2902", "service_id": "", }
        result = open_wpv_2901(lock, pub_socket, data, open_param)
        message["result"] = result
        sync_check_algorith_result(data, detail, message)
        result = close_wpv_2902(lock, pub_socket, data, close_param)
        # message["result"] = result
        # sync_check_algorith_stop_result(data, detail, message)


def Test_Multiple_Algorith_001(lock, pub_socket, data, detail, params):
    """
    同时触发PPP、WL、RSDS算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        ppp_1401_open_param = {"step": "1401", "service_id": "", "params": json.dumps({"station_type": "2"})}
        ppp_1401_message = {"command": "AEC-PPP", "result": {}, "delay": 4}
        ppp_1402_close_param = {"step": "1402", "service_id": "", }
        wl_2401_open_param_1 = {"step": "2401", "service_id": "", "params": json.dumps({"auth_step": "1"})}
        wl_2401_open_param_2 = {"step": "2401", "service_id": "", "params": json.dumps({"auth_step": "2"})}
        wl_2401_open_param_3 = {"step": "2401",
                                "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
                                "params": json.dumps({"auth_step": "3"})}
        wl_2401_message = {"command": "AEC-WL", "result": {}, "delay": 4}
        wl_2402_close_param = {"step": "2402", "service_id": "", }
        rsds_2601_open_param_1 = {"step": "2601", "service_id": "", "params": json.dumps({})}
        rsds_2601_open_param_2 = {"step": "2601", "service_id": "", "params": json.dumps({"door_action": "1"})}
        rsds_2601_message = {"command": "AEC-RSDS", "result": {}, "delay": 15}
        rsds_2602_close_param = {"step": "2602", "service_id": "", }
    else:
        msg = f"params not get correct version:{version}, not support"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)
        return
    result = open_ppp_1401(lock, pub_socket, data, ppp_1401_open_param)
    ppp_1401_message["result"] = result
    sync_check_algorith_result(data, detail, ppp_1401_message)
    result = open_wl_2401(lock, pub_socket, data, wl_2401_open_param_1)
    wl_2401_message["result"] = result
    sync_check_algorith_result(data, detail, wl_2401_message)
    result = open_wl_2401(lock, pub_socket, data, wl_2401_open_param_2)
    time.sleep(random.randint(1, 3))
    result = open_wl_2401(lock, pub_socket, data, wl_2401_open_param_3)
    open_rsds_2601(lock, pub_socket, data, rsds_2601_open_param_1)
    time.sleep(random.randint(1, 2))
    result = open_rsds_2601(lock, pub_socket, data, rsds_2601_open_param_2)
    rsds_2601_message["result"] = result
    sync_check_algorith_result(data, detail, rsds_2601_message)
    result = close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param)
    ppp_1401_message["result"] = result
    sync_check_algorith_stop_result(data, detail, ppp_1401_message)
    result = close_wl_2402(lock, pub_socket, data, wl_2402_close_param)
    wl_2401_message["result"] = result
    sync_check_algorith_stop_result(data, detail, wl_2401_message)
    result = close_rsds_2602(lock, pub_socket, data, rsds_2602_close_param)
    rsds_2601_message["result"] = result
    sync_check_algorith_stop_result(data, detail, rsds_2601_message)


def Test_Multiple_Algorith_002(lock, pub_socket, data, detail, params):
    """
    同时触发PiP、ViP、VBSL算法，并收集对仿真照片的结果
    :param lock:
    :param pub_socket:
    :param data:
    :param detail:
    :param params
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        pip_1301_open_param = {"step": "1301", "service_id": "",
                               "params": json.dumps({"vehicle_type": "ES6",
                                                     "is_unmanned_station": "1",
                                                     "station_type": "2"})}
        pip_1301_message = {"command": "AEC-PiP", "result": {}, "delay": 4}
        pip_1302_close_param = {"step": "1302", "service_id": "", }
        vip2_2201_open_param = {"step": "2201", "service_id": "", "params": json.dumps({"is_rsdv": "0"})}
        vip2_2201_message = {"command": "AEC-ViP", "result": {}, "delay": 15}
        vip2_2202_close_param = {"step": "2202", "service_id": "", }
    else:
        msg = f"params not get correct version:{version}, not support"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)
        return
    result = open_pip_1301(lock, pub_socket, data, pip_1301_open_param)
    pip_1301_message["result"] = result
    check_algorith_result(data, detail, pip_1301_message)
    result = open_vip2_2201(lock, pub_socket, data, vip2_2201_open_param)
    vip2_2201_message["result"] = result
    sync_check_algorith_result(data, detail, vip2_2201_message)
    result = close_pip_1302(lock, pub_socket, data, pip_1302_close_param)
    pip_1301_message["result"] = result
    result = close_vip2_2202(lock, pub_socket, data, vip2_2202_close_param)
    vip2_2201_message["result"] = result
    sync_check_algorith_stop_result(data, detail, pip_1301_message)
    sync_check_algorith_stop_result(data, detail, vip2_2201_message)


def Test_Normal_SwapBattery_001(lock, pub_socket, data, detail, params):
    """
    根据换电流程和算法调用映射表（MCS事件与AEC算法启停映射 ），模拟整个换电过程，触发算法，并收集对仿真照片的结果
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    version = int(params.get("version", 3))
    if version == 3:
        bbsa_1001_open_param_1 = {"step": "1001",
                                  "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
                                  "params": json.dumps({"battery_type": "2", "station_type": "2", })}
        bbsa_1001_open_param_2 = {"step": "1001",
                                  "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
                                  "params": json.dumps({"battery_type": "1", "station_type": "2", })}
        bbsa_1001_message = {"command": "AEC-BBSA", "result": {}, "delay": 4}
        bbsa_1002_close_param = {"step": "1002", "service_id": "", }

        bsa_1101_open_param_1 = {"step": "1101",
                                 "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
                                 "params": json.dumps({"battery_type": "1",
                                                       "station_type": "2",
                                                       "battery_bms_pack_id": "P0079340AP33620006130X001A00014"
                                                       })}
        bsa_1101_open_param_2 = {"step": "1101",
                                 "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
                                 "params": json.dumps({"battery_type": "2",
                                                       "station_type": "2",
                                                       "battery_bms_pack_id": "P0079340AP33620006130X001A00015"
                                                       })}
        bsa_1101_message = {"command": "AEC-BSA", "result": {}, "delay": 4}
        bsa_1102_close_param = {"step": "1102", "service_id": "", }

        pip_1301_open_param = {"step": "1301", "service_id": "",
                               "params": json.dumps({"vehicle_type": "ES6",
                                                     "is_unmanned_station": "1",
                                                     "station_type": "2"})}
        pip_1301_message = {"command": "AEC-PiP", "result": {}, "delay": 10}
        pip_1302_close_param = {"step": "1302", "service_id": "", }

        ppp_1401_open_param = {"step": "1401", "service_id": "", "params": json.dumps({"station_type": "2"})}
        ppp_1401_message = {"command": "AEC-PPP", "result": {}, "delay": 4}
        ppp_1402_close_param = {"step": "1402", "service_id": "", }

        vip2_2201_open_param_1 = {"step": "2201", "service_id": "", "params": json.dumps({"is_rsdv": "0"})}
        vip2_2201_open_param_2 = {"step": "2201", "service_id": "", "params": json.dumps({"is_rsdv": "1"})}
        vip2_2201_message = {"command": "AEC-ViP", "result": {}, "delay": 15}
        vip2_2202_close_param = {"step": "2202", "service_id": "", }

        wl_2401_open_param_1 = {"step": "2401", "service_id": "", "params": json.dumps({"auth_step": "1"})}
        wl_2401_open_param_2 = {"step": "2401", "service_id": "", "params": json.dumps({"auth_step": "2"})}
        wl_2401_open_param_3 = {"step": "2401",
                                "service_id": "PS-NIO-0e434939-37e7e4d2acb2e48b875845aabdf032bf9eaf01441688051918050",
                                "params": json.dumps({"auth_step": "3"})}
        wl_2401_message = {"command": "AEC-WL", "result": {}, "delay": 4}
        wl_2402_close_param = {"step": "2402", "service_id": "", }

        rsds_2601_open_param_1 = {"step": "2601", "service_id": "", "params": json.dumps({})}
        rsds_2601_open_param_2 = {"step": "2601", "service_id": "", "params": json.dumps({"door_action": "1"})}
        rsds_2601_open_param_3 = {"step": "2601", "service_id": "", "params": json.dumps({"door_action": "0"})}
        rsds_2601_message = {"command": "AEC-RSDS", "result": {}, "delay": 15}
        rsds_2602_close_param = {"step": "2602", "service_id": "", }

        wpv_2901_open_param = {"step": "2901", "service_id": "", "params": ""}
        wpv_2901_message = {"command": "AEC-WPV", "result": {}, "delay": 10}
        wpv_2902_close_param = {"step": "2902", "service_id": "", }

        open_rsds_2601(lock, pub_socket, data, rsds_2601_open_param_1)
        time.sleep(random.randint(1, 2))
        result = open_rsds_2601(lock, pub_socket, data, rsds_2601_open_param_2)
        rsds_2601_message["result"] = result
        check_algorith_result(data, detail, rsds_2601_message)

        time.sleep(random.randint(6, 10))
        close_pip_1302(lock, pub_socket, data, pip_1302_close_param)
        close_vip2_2202(lock, pub_socket, data, vip2_2202_close_param)

        time.sleep(random.randint(10, 15))  # 实际要等待很久
        result = open_wl_2401(lock, pub_socket, data, wl_2401_open_param_1)
        wl_2401_message["result"] = result
        check_algorith_result(data, detail, wl_2401_message)

        result = open_ppp_1401(lock, pub_socket, data, ppp_1401_open_param)
        ppp_1401_message["result"] = result
        check_algorith_result(data, detail, ppp_1401_message)

        result = open_rsds_2601(lock, pub_socket, data, rsds_2601_open_param_2)
        rsds_2601_message["result"] = result
        check_algorith_result(data, detail, rsds_2601_message)

        time.sleep(random.randint(5, 10))
        close_pip_1302(lock, pub_socket, data, pip_1302_close_param)
        close_vip2_2202(lock, pub_socket, data, vip2_2202_close_param)

        result = open_wpv_2901(lock, pub_socket, data, wpv_2901_open_param)
        wpv_2901_message["result"] = result
        check_algorith_result(data, detail, wpv_2901_message)

        close_wpv_2902(lock, pub_socket, data, wpv_2902_close_param)  # 执行后没有等待，立即执行2401

        result = open_wl_2401(lock, pub_socket, data, wl_2401_open_param_2)
        wl_2401_message["result"] = result
        check_algorith_result(data, detail, wl_2401_message)

        time.sleep(random.randint(4, 6))
        close_rsds_2602(lock, pub_socket, data, rsds_2602_close_param)
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param)

        result = open_wl_2401(lock, pub_socket, data, wl_2401_open_param_3)
        wl_2401_message["result"] = result
        check_algorith_result(data, detail, wl_2401_message)
        time.sleep(random.randint(1, 3))
        close_wl_2402(lock, pub_socket, data, wl_2402_close_param)

        result = open_pip_1301(lock, pub_socket, data, pip_1301_open_param)
        pip_1301_message["result"] = result
        check_algorith_result(data, detail, pip_1301_message)

        time.sleep(random.randint(15, 20))
        result = open_bbsa_1001(lock, pub_socket, data, bbsa_1001_open_param_1)
        bbsa_1001_message["result"] = result
        check_algorith_result(data, detail, bbsa_1001_message)

        time.sleep(random.randint(1, 2))
        close_bbsa_1002(lock, pub_socket, data, bbsa_1002_close_param)

        time.sleep(random.randint(10, 20))
        result = open_bsa_1101(lock, pub_socket, data, bsa_1101_open_param_1)
        bsa_1101_message["result"] = result
        check_algorith_result(data, detail, bsa_1101_message)

        time.sleep(random.randint(1, 3))
        close_bsa_1102(lock, pub_socket, data, bsa_1102_close_param)

        time.sleep(random.randint(10, 20))
        result = open_bbsa_1001(lock, pub_socket, data, bbsa_1001_open_param_2)
        bbsa_1001_message["result"] = result
        check_algorith_result(data, detail, bbsa_1001_message)

        time.sleep(random.randint(1, 2))
        close_bbsa_1002(lock, pub_socket, data, bbsa_1002_close_param)

        time.sleep(random.randint(5, 10))
        close_pip_1302(lock, pub_socket, data, pip_1302_close_param)

        time.sleep(random.randint(5, 10))
        result = open_vip2_2201(lock, pub_socket, data, vip2_2201_open_param_1)
        vip2_2201_message["result"] = result
        check_algorith_result(data, detail, vip2_2201_message)

        time.sleep(random.randint(5, 10))
        result = open_bsa_1101(lock, pub_socket, data, bsa_1101_open_param_2)
        bsa_1101_message["result"] = result
        check_algorith_result(data, detail, bsa_1101_message)

        time.sleep(random.randint(1, 2))
        close_bsa_1102(lock, pub_socket, data, bsa_1102_close_param)

        time.sleep(random.randint(5, 15))
        close_vip2_2202(lock, pub_socket, data, vip2_2202_close_param)  # 关闭后还是有2201的数据

        open_rsds_2601(lock, pub_socket, data, rsds_2601_open_param_1)
        time.sleep(random.randint(1, 2))
        open_rsds_2601(lock, pub_socket, data, rsds_2601_open_param_3)

        result = open_pip_1301(lock, pub_socket, data, pip_1301_open_param)
        pip_1301_message["result"] = result
        check_algorith_result(data, detail, pip_1301_message)

        result = open_vip2_2201(lock, pub_socket, data, vip2_2201_open_param_2)
        vip2_2201_message["result"] = result
        check_algorith_result(data, detail, vip2_2201_message)

        time.sleep(random.randint(15, 20))
        close_pip_1302(lock, pub_socket, data, pip_1302_close_param)
        close_vip2_2202(lock, pub_socket, data, vip2_2202_close_param)
    else:
        bbsa_1001_open_param_1 = {"step": "1001",
                                  "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                  "params": json.dumps(
                                      {"vehicle_type": "EC6",
                                       "battery_type": "70",
                                       "is_unmanned_station": "1",
                                       "station_type": "1",
                                       "locate_stage": "2"})}
        bbsa_1001_open_param_2 = {"step": "1001",
                                  "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                  "params": json.dumps({
                                      "vehicle_type": "EC6",
                                      "battery_type": "70",
                                      "filter": {
                                          "id": ["6", "7", "8", "3", "4", "5"],
                                          "count": "1",
                                          "lower": "0.2",
                                          "upper": "1.0",
                                          "threshold": "0.8"},
                                      "is_unmanned_station": "1",
                                      "station_type": "1",
                                      "locate_stage": "1"})}
        bbsa_1001_message = {"command": "BBSA", "result": {}, "delay": 10}

        bsa_1101_open_param_1 = {"step": "1101",
                                 "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                 "params": json.dumps({
                                     "vehicle_type": "EC6",
                                     "battery_type": "70",
                                     "is_unmanned_station": "1",
                                     "station_type": "1",
                                     "locate_stage": "1",
                                     "battery_bms_pack_id": "P0079340AK081200061300001A00030"
                                 })}
        bsa_1101_open_param_2 = {"step": "1101",
                                 "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                 "params": json.dumps({"battery_type": "70",
                                                       "station_type": "1",
                                                       "locate_stage": "2",
                                                       "battery_bms_pack_id": "P0079340AP008210061100071A00047"
                                                       })}
        bsa_1101_message = {"command": "BATTERY-UP-SURFACE-CHECK", "result": {}, "delay": 10}

        bscc_1201_open_param = {"step": "1201",
                                "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                "params": json.dumps({
                                    "vehicle_type": "EC6",
                                    "battery_type": "70",
                                    "is_unmanned_station": "1",
                                    "station_type": "1",
                                    "locate_stage": "1",
                                    "battery_bms_pack_id": "P0079340AK081200061300001A00030"
                                })}
        bscc_1201_message = {"command": "BATTERY-SURFACE-CAMERA-CHECK", "result": {}, "delay": 10}

        pip_1301_open_param_1 = {"step": "1301", "service_id": "",
                                 "params": json.dumps({"vehicle_type": "EC6",
                                                       "battery_type": "",
                                                       "is_unmanned_station": "1",
                                                       "station_type": "1"})}
        pip_1301_open_param_2 = {"step": "1301",
                                 "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                 "params": json.dumps({"vehicle_type": "EC6",
                                                       "battery_type": "70",
                                                       "is_unmanned_station": "1",
                                                       "station_type": "1",
                                                       "locate_stage": "2"})}
        pip_1301_open_param_3 = {"step": "1301",
                                 "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                 "params": json.dumps({"vehicle_type": "EC6",
                                                       "battery_type": "70",
                                                       "is_unmanned_station": "1",
                                                       "station_type": "1",
                                                       "locate_stage": "1",
                                                       "battery_bms_pack_id": "P0079340AK081200061300001A00030"})}
        pip_1301_open_param_4 = {"step": "1301",
                                 "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                 "params": json.dumps({
                                     "vehicle_type": "EC6",
                                     "battery_type": "70",
                                     "filter": {
                                         "id": ["6", "7", "8", "3", "4", "5"],
                                         "count": "1",
                                         "lower": "0.2",
                                         "upper": "1.0",
                                         "threshold": "0.8"},
                                     "is_unmanned_station": "1",
                                     "station_type": "1",
                                     "locate_stage": "1"
                                 })}
        pip_1301_message = {"command": "HUMAN-ACTIVITY", "result": {}, "delay": 10}
        pip_1302_close_param_1 = {"step": "1302", "service_id": "", "params": ""}
        pip_1302_close_param_2 = {"step": "1302",
                                  "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                  "params": ""}

        ppp_1401_open_param = {"step": "1401", "service_id": "", "params": json.dumps({"station_type": "1"})}
        ppp_1401_message = {"command": "PARKING-HUMAN-DETECTION", "result": {}, "delay": 4}
        ppp_1402_close_param_1 = {"step": "1402", "service_id": "", "params": ""}
        ppp_1402_close_param_2 = {"step": "1402",
                                  "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                  "params": ""}

        rsdv_pip_1501_open_param = {"step": "1501",
                                    "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                    "params": json.dumps({
                                        "vehicle_type": "",
                                        "station_type": "1"
                                    })}
        rsdv_pip_1502_close_param = {"step": "1502",
                                     "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                     "params": json.dumps({
                                         "vehicle_type": "",
                                         "station_type": "1"
                                     })}
        rsdv_pip_1501_message = {"command": "RSDV_PiP", "result": {}, "delay": 10}

        rsdv_vlsv_1601_open_param = {"step": "1601",
                                     "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                     "params": ""}

        rsdv_vlsv_1602_close_param = {"step": "1602",
                                      "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                      "params": ""}

        rsdv_vlsv_1601_message = {"command": "RSDV_VLSV2", "result": {}, "delay": 10}

        smd_1701_open_param = {"step": "1701",
                               "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                               "params": json.dumps({
                                   "vehicle_type": "EC6",
                                   "battery_type": "70",
                                   "filter": {
                                       "id": ["6", "7", "8", "3", "4", "5"],
                                       "count": "1",
                                       "lower": "0.2",
                                       "upper": "1.0",
                                       "threshold": "0.8"},
                                   "is_unmanned_station": "1",
                                   "station_type": "1",
                                   "locate_stage": "1"
                               })}
        smd_1701_message = {"command": "SCREW-SOCKET-MISSING", "result": {}, "delay": 10}

        vip2_2201_open_param = {"step": "2201",
                                "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                "params": json.dumps({"vehicle_type": "EC6", "station_type": "1"})}
        vip2_2201_message = {"command": "CAR-IN-PLATFORM", "result": {}, "delay": 15}
        vip2_2202_close_param = {"step": "2202",
                                 "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                 "params": ""}

        vor_2301_open_param = {"step": "2301",
                               "service_id": "",
                               "params": json.dumps({"vehicle_type": "", "station_type": "1", })}
        vor_2301_message = {"command": "VOR", "result": {}, "delay": 10}

        wl_2401_open_param_1 = {"step": "2401", "service_id": "", "params": json.dumps({"station_type": "1"})}
        wl_2401_open_param_2 = {"step": "2401", "service_id": "",
                                "params": json.dumps({"vehicle_type": "", "auth_step": "2"})}
        wl_2401_open_param_3 = {"step": "2401", "service_id": "",
                                "params": json.dumps({"vehicle_type": "", "station_type": "1"})}
        wl_2401_open_param_4 = {"step": "2401", "service_id": "",
                                "params": json.dumps({"vehicle_type": "EC6", "station_type": "1"})}
        wl_2401_message = {"command": "WHEEL-LOCATE", "result": {}, "delay": 10}
        wl_2402_close_param_1 = {"step": "2402", "service_id": "", "params": ""}
        wl_2402_close_param_2 = {"step": "2402",
                                 "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                 "params": ""}

        wlcc_2501_open_param = {"step": "2501",
                                "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                "params": json.dumps({"vehicle_type": "EC6", "station_type": "1"})}
        wlcc_2501_message = {"command": "WHEEL-LOCATE-CAMERA-CHECK", "result": {}, "delay": 10}

        rsds_2601_open_param = {"step": "2601",
                                "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                "params": json.dumps({"vehicle_type": "EC6", "station_type": "1"})}
        rsds_2601_message = {"command": "RSDS", "result": {}, "delay": 15}
        rsds_2602_close_param = {"step": "2602", "service_id": "", "params": ""}

        sapa_2701_open_param = {"step": "2701",
                                "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                "params": json.dumps({
                                    "station_type": "1",
                                    "is_unmanned_station": "1",
                                    "park_direction": "0"
                                })}
        sapa_2702_close_param = {"step": "2702", "service_id": "", "params": ""}
        sapa_2701_message = {"command": "SAPA", "result": {}, "delay": 10}

        bbcc_2801_open_param = {"step": "2801",
                                "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
                                "params": json.dumps({
                                    "vehicle_type": "EC6",
                                    "battery_type": "70",
                                    "filter": {
                                        "id": ["6", "7", "8", "3", "4", "5"],
                                        "count": "1",
                                        "lower": "0.2",
                                        "upper": "1.0",
                                        "threshold": "0.8"},
                                    "is_unmanned_station": "1",
                                    "station_type": "1",
                                    "locate_stage": "1"
                                })}
        bbcc_2801_message = {"command": "BBCC", "result": {}, "delay": 10}

        wpv_2901_open_param = {"step": "2901", "service_id": "",
                               "params": json.dumps({"station_type": "1", "vehicle_type": ""})}
        wpv_2901_message = {"command": "WPV", "result": {}, "delay": 10}
        wpv_2902_close_param = {"step": "2902", "service_id": "", "params": ""}

        lsd_3101_open_param = {
            "step": "3101",
            "service_id": "PS-NIO-0c10740e-c2791df0b153a3f5d67b4576a88aab389784895e1693204570729",
            "params": json.dumps({"light_action": "1", "station_type": "1"})
        }
        lsd_1301_message = {"command": "LSD", "result": {}, "delay": 10}

        log.info("<STEP_1>:泊车开始")
        close_pip_1302(lock, pub_socket, data, pip_1302_close_param_1)
        result = open_ppp_1401(lock, pub_socket, data, ppp_1401_open_param)
        ppp_1401_message["result"] = result
        result = open_wl_2401(lock, pub_socket, data, wl_2401_open_param_1)
        wl_2401_message["result"] = result
        check_algorith_result(data, detail, ppp_1401_message, ver=2)
        check_algorith_result(data, detail, wl_2401_message, ver=2)

        time.sleep(random.randint(10, 15))
        log.info("<STEP_2>:车机鉴权")
        result = open_vor_2301(lock, pub_socket, data, vor_2301_open_param)
        vor_2301_message["result"] = result
        check_algorith_result(data, detail, vor_2301_message, ver=2)
        close_rsds_2602(lock, pub_socket, data, rsds_2602_close_param)
        close_sapa_2702(lock, pub_socket, data, sapa_2702_close_param)
        open_wl_2401(lock, pub_socket, data, wl_2401_open_param_2)
        result = open_wpv_2901(lock, pub_socket, data, wpv_2901_open_param)
        wpv_2901_message["result"] = result
        check_algorith_result(data, detail, wpv_2901_message, ver=2)
        time.sleep(1)
        close_pip_1302(lock, pub_socket, data, pip_1302_close_param_1)
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param_1)
        log.info("<STEP_3>:启动换电按键使能")
        close_wpv_2902(lock, pub_socket, data, wpv_2902_close_param)
        open_wl_2401(lock, pub_socket, data, wl_2401_open_param_3)
        time.sleep(3)
        close_pip_1302(lock, pub_socket, data, pip_1302_close_param_1)
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param_1)
        result = open_wl_2401(lock, pub_socket, data, wl_2401_open_param_4)
        wl_2401_message["result"] = result
        check_algorith_result(data, detail, wl_2401_message, ver=2)

        time.sleep(random.randint(10, 15))
        log.info("<STEP_4>:y对中")
        close_wl_2402(lock, pub_socket, data, wl_2402_close_param_1)
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param_1)
        result = open_pip_1301(lock, pub_socket, data, pip_1301_open_param_1)
        pip_1301_message["result"] = result
        check_algorith_result(data, detail, pip_1301_message, ver=2)

        time.sleep(random.randint(10, 15))
        log.info("<STEP_5>:车辆电池下表面拍照开始")
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param_2)
        result = open_bbsa_1001(lock, pub_socket, data, bbsa_1001_open_param_1)
        bbsa_1001_message["result"] = result
        open_pip_1301(lock, pub_socket, data, pip_1301_open_param_2)
        check_algorith_result(data, detail, bbsa_1001_message, ver=2)

        time.sleep(random.randint(1, 3))
        log.info("<STEP_6>:服务电池上表面拍照开始")
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param_2)
        result = open_bsa_1101(lock, pub_socket, data, bsa_1101_open_param_1)
        bsa_1101_message["result"] = result
        result = open_bscc_1201(lock, pub_socket, data, bscc_1201_open_param)
        bscc_1201_message["result"] = result
        result = open_pip_1301(lock, pub_socket, data, pip_1301_open_param_3)
        pip_1301_message["result"] = result
        result = open_lsd_3101(lock, pub_socket, data, lsd_3101_open_param)
        lsd_1301_message["result"] = result
        check_algorith_result(data, detail, bsa_1101_message, ver=2)
        check_algorith_result(data, detail, bscc_1201_message, ver=2)
        check_algorith_result(data, detail, pip_1301_message, ver=2)
        # 处于shadow的模式的算法，不进行检测
        # check_algorith_result(data, detail, lsd_1301_message, ver=2)

        time.sleep(random.randint(10, 15))
        log.info("<STEP_7>:服务电池下表面拍照开始")
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param_2)
        result = open_bbsa_1001(lock, pub_socket, data, bbsa_1001_open_param_2)
        bbsa_1001_message["result"] = result
        result = open_pip_1301(lock, pub_socket, data, pip_1301_open_param_4)
        pip_1301_message["result"] = result
        result = open_smd_1701(lock, pub_socket, data, smd_1701_open_param)
        smd_1701_message["result"] = result
        open_bbcc_2801(lock, pub_socket, data, bbcc_2801_open_param)
        check_algorith_result(data, detail, bbsa_1001_message, ver=2)
        check_algorith_result(data, detail, pip_1301_message, ver=2)
        check_algorith_result(data, detail, smd_1701_message, ver=2)

        time.sleep(random.randint(10, 15))
        log.info("<STEP_8>:车辆电池上表面拍照开始")
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param_2)
        result = open_bsa_1101(lock, pub_socket, data, bsa_1101_open_param_2)
        bsa_1101_message["result"] = result
        check_algorith_result(data, detail, bsa_1101_message, ver=2)

        time.sleep(random.randint(10, 15))
        log.info("<STEP_9>:车辆上高压")
        close_pip_1302(lock, pub_socket, data, pip_1302_close_param_2)
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param_2)
        result = open_vip2_2201(lock, pub_socket, data, vip2_2201_open_param)
        vip2_2201_message["result"] = result
        check_algorith_result(data, detail, vip2_2201_message, ver=2)

        time.sleep(random.randint(10, 15))
        log.info("<STEP_10>:换电完成")
        close_pip_1302(lock, pub_socket, data, pip_1302_close_param_2)
        close_wl_2402(lock, pub_socket, data, wl_2402_close_param_2)
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param_2)
        result = open_vip2_2201(lock, pub_socket, data, vip2_2201_open_param)
        vip2_2201_message["result"] = result
        check_algorith_result(data, detail, vip2_2201_message, ver=2)

        time.sleep(random.randint(10, 15))
        log.info("<STEP_11>:车辆驶离")
        result = open_sapa_2701(lock, pub_socket, data, sapa_2701_open_param)
        open_sapa_2701(lock, pub_socket, data, sapa_2701_open_param)
        sapa_2701_message["result"] = result
        check_algorith_result(data, detail, sapa_2701_message, ver=2)
        time.sleep(random.randint(3, 5))
        close_pip_1302(lock, pub_socket, data, pip_1302_close_param_2)
        close_ppp_1402(lock, pub_socket, data, ppp_1402_close_param_2)
        close_vip2_2202(lock, pub_socket, data, vip2_2202_close_param)

        result = open_wlcc_2501(lock, pub_socket, data, wlcc_2501_open_param)
        wlcc_2501_message["result"] = result
        result = open_rsds_2601(lock, pub_socket, data, rsds_2601_open_param)
        rsds_2601_message["result"] = result
        # 待开发确认，暂时先不检查 ### 待修改连续运行三次
        # check_algorith_result(data, detail, wlcc_2501_message, ver=2)
        check_algorith_result(data, detail, rsds_2601_message, ver=2)
        time.sleep(random.randint(1, 2))
        if int(time.time() * 1000) % 2:
            log.info("<STEP_12>:卷帘门关闭开始检测")
            result = open_rsdv_pip_1501(lock, pub_socket, data, rsdv_pip_1501_open_param)
            rsdv_pip_1501_message["result"] = result
            result = open_rsdv_vlsv2_1601(lock, pub_socket, data, rsdv_vlsv_1601_open_param)
            rsdv_vlsv_1601_message["result"] = result
            check_algorith_result(data, detail, rsdv_pip_1501_message, ver=2)
            check_algorith_result(data, detail, rsdv_vlsv_1601_message, ver=2)
            time.sleep(random.randint(3, 5))
            close_rsdv_pip_1502(lock, pub_socket, data, rsdv_pip_1502_close_param)
            close_rsdv_vlsv2_1602(lock, pub_socket, data, rsdv_vlsv_1602_close_param)
        result = open_sapa_2701(lock, pub_socket, data, sapa_2701_open_param)
        open_sapa_2701(lock, pub_socket, data, sapa_2701_open_param)
        sapa_2701_message["result"] = result
        # check_algorith_result(data, detail, sapa_2701_message)
        time.sleep(random.randint(10, 15))


def Test_Abnormal_SwapBattery_001(lock, pub_socket, data, detail, params):
    version = int(params.get("version", 3))
    if version == 3:
        rsds_2601_open_param_1 = {"step": "2601", "service_id": "", "params": json.dumps({})}
        rsds_2601_open_param_2 = {"step": "2601", "service_id": "", "params": json.dumps({"door_action": "1"})}
        rsds_2602_close_param = {"step": "2602", "service_id": "", }
    else:
        msg = f"params not get correct version:{version}, not support"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)
        return
    close_rsds_2602(lock, pub_socket, data, rsds_2602_close_param)
    time.sleep(random.randint(10, 15))
    open_rsds_2601(lock, pub_socket, data, rsds_2601_open_param_1)
    time.sleep(random.randint(3, 5))
    open_rsds_2601(lock, pub_socket, data, rsds_2601_open_param_2)
    time.sleep(random.randint(5, 10))


def Test_Random_Algorith_001(lock, pub_socket, data, detail, params):
    """
        模拟发送随机命令操作
    :param pub_socket:
    :param data:
    :param detail:
    :param params:
    :return:
    """
    algorith = {"bbsa": Test_Single_Algorith_001,
                "bsa": Test_Single_Algorith_002,
                "pip": Test_Single_Algorith_004,
                "ppp": Test_Single_Algorith_005,
                "vip2": Test_Single_Algorith_013,
                "wl": Test_Single_Algorith_015,
                "rsds": Test_Single_Algorith_017,
                "wpv": Test_Single_Algorith_020
                }
    names = ["bbsa", "bsa", "pip", "ppp", "vip2", "wl", "rsds", "wpv"]
    random.shuffle(names)
    with ThreadPoolExecutor(max_workers=3, thread_name_prefix='Random_Algorith') as pool:
        all_task = []
        for name in names:
            all_task.append(pool.submit(algorith.get(name), lock, pub_socket, data, detail, params))
        for future in as_completed(all_task):
            future.result()
