"""
@Author: wenlong.jin
@File: algorith_utils.py
@Project: aec-test
@Time: 2023/7/7 13:43
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
import functools
import threading
from utils import log

msg_topic = b"MCS"
msg_type = b"INFO"
msg_command = b"STEP"


def sync_check_algorith_stop_result(data, detail, message):
    """
    同步检查算法关闭后在指定的时间间隔内 HB发送的算法的运行状态是否关闭
    :param data:
    :param detail:
    :param message:
    :return:
    """
    command = message.get("command")
    timestamp = message["result"].get("timestamp")
    delay = message.get("delay")
    for i in range(delay):
        if command in detail["HB"]["comment"] and detail["HB"]["comment"][command] == 0:
            log.debug(f"MCS {command} success receive {command} stop result from AEC HB")
            break
        elif command not in detail["HB"]["comment"]:
            log.warning(f'{command}, ---> {detail["HB"]["comment"]}')
        time.sleep(1)
    else:
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp / 1000)))
        msg = f"MCS_systime:{time_str} MCS stop {command}, during {delay}s not receive stop result from AEC HB"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)


def sync_check_algorith_result(data, detail, message):
    """
    同步检查算法打开的结果
    :param data:
    :param detail:
    :param message
    :return:
    """
    command = message.get("command")
    timestamp = message["result"].get("timestamp")
    delay = message.get("delay")
    for i in range(delay):
        # 实际调试发现模拟mcs的系统和AEC系统存在时间误差，这里加了2s
        if command in detail and detail[command]["timestamp"] + 2000 > timestamp:
            log.debug(f"MCS {command} success receive result data from AEC")
            break
        time.sleep(1)
    else:
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp / 1000)))
        msg = f"MCS_systime:{time_str} MCS {command} algorith start, during {delay}s not receive data from AEC"
        log.error(msg)
        data["result"] = "FAIL"
        data["data"].append(msg)


def check_algorith_stop_result(data, detail, message):
    """

    :param data:
    :param detail:
    :param message
    :return:
    """

    def _check_result(_data, _detail, _message):
        command = _message.get("command")
        timestamp = _message["result"].get("timestamp")
        delay = _message.get("delay")
        for i in range(delay):
            if command in _detail["HB"]["comment"] and _detail["HB"]["comment"][command] == 0:
                log.debug(f"MCS {command} success receive {command} stop result from AEC HB")
                break
            elif command not in _detail["HB"]["comment"]:
                log.warning(f'{command}, ---> {_detail["HB"]["comment"]}')
            time.sleep(1)
        else:
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp / 1000)))
            msg = f"MCS_systime:{time_str} MCS stop {command}, during {delay}s not receive stop result from AEC HB"
            log.error(msg)
            _data["result"] = "FAIL"
            _data["data"].append(msg)

    th = threading.Thread(target=_check_result, args=(data, detail, message))
    th.daemon = True
    th.start()
    th.join(0.001)


def check_algorith_result(data, detail, message, ver=3):
    """
    异步检查算法打开的执行结果
    :param data:
    :param detail:
    :param message
    :param ver
    :return:
    """

    def _check_result(_data, _detail, _message):
        command = _message.get("command")
        timestamp = _message["result"].get("timestamp")
        delay = _message.get("delay")
        flag = False
        for i in range(delay):
            # 实际调试发现模拟mcs的系统和AEC系统存在时间误差，这里加了2s
            if command in _detail and _detail[command]["timestamp"] + 2000 > timestamp:
                comment = _detail[command]["comment"].get("result")
                # 检查算法的运行结果
                if comment == -1:
                    flag = True
                    continue
                log.debug(f"MCS {command} success receive result data from AEC, and result is {comment}")
                return
            time.sleep(1)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp / 1000)))
        if flag:
            _info = "not receive correct result from AEC"
        else:
            _info = "not receive result data from AEC"
        msg = f"MCS_systime:{time_str} {command} algorith start, during {delay}s {_info}"
        log.error(msg)
        _data["result"] = "FAIL"
        _data["data"].append(msg)
    # 检查各个相机的状态, 这里需要修改，避免
    # camera_state = [1, ] if ver == 3 else [0, ]  # 二代站不为0，代表相机掉线或者分辨率不对，三代站不为1代表相机工作不正常
    # if detail.get("HB"):
    #     _comment = detail["HB"]["comment"]
    #     for key, val in _comment.items():
    #         if key.startswith("camera") and int(val) not in camera_state:
    #             time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    #             msg = f"MCS_systime:{time_str} AEC HB, {key} work state is {val}"
    #             log.error(msg)
    #             data["result"] = "FAIL"
    #             data["data"].append(msg)
    th = threading.Thread(target=_check_result, args=(data, detail, message))
    th.daemon = True
    th.start()
    th.join(0.001)


def _algorithm(func):
    """
    发送对应的步骤信息，并通过data进行各步骤状态的检查和判断
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(lock, pub_socket, data, param, *args, **kwargs):
        log.debug(f"{func.__name__} begin execute ...")
        timestamp = int(time.time() * 1000)
        msg_timestamp = bytes(str(timestamp), encoding='utf-8')
        msg_comment = bytes(json.dumps(param), encoding='utf-8')
        msg_data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
        with lock:
            log.debug(f"{func.__name__} send topic data ...")
            pub_socket.send_multipart(msg_data)
        func(lock, pub_socket, data, param, *args, **kwargs)
        log.debug(f"{func.__name__} execute success ...")
        return {"timestamp": timestamp}

    return wrapper


@_algorithm
def open_rsds_2601(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # # _comment = {"step": "2601", "service_id": "", "params": json.dumps(params)}
    # msg_comment = bytes(json.dumps(param), encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def close_rsds_2602(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # _comment = {"step": "2602", "service_id": ""}
    # msg_comment = bytes(json.dumps(_comment), encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def open_rsdv_pip_1501(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # msg_comment = bytes(json.dumps({"step": "1501", "service_id": "",
    #                                 "params": json.dumps(
    #                                     {"vehicle_type": "", "is_unmanned_station": "", "station_type": "2"})}),
    #                     encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def close_rsdv_pip_1502(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # _comment = {"step": "1502", "service_id": "", }
    # msg_comment = bytes(json.dumps(_comment), encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def open_vip2_2201(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # msg_comment = bytes(json.dumps({"step": "2201", "service_id": service_id, "params": ""}),
    #                     encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def close_vip2_2202(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # _comment = {"step": "2202", "service_id": "", }
    # msg_comment = bytes(json.dumps(_comment), encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def open_wl_2401(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # msg_comment = bytes(
    #     json.dumps({"step": "2401", "service_id": service_id, "params": json.dumps({"auth_step": auth_step})}),
    #     encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.02)


@_algorithm
def close_wl_2402(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # _comment = {"step": "2402", "service_id": "", }
    # msg_comment = bytes(json.dumps(_comment), encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.02)


@_algorithm
def open_ppp_1401(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # msg_comment = bytes(json.dumps({"step": "1401", "service_id": "", "params": json.dumps({"station_type": "2"})}),
    #                     encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def close_ppp_1402(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # _comment = {"step": "1402", "service_id": "", }
    # msg_comment = bytes(json.dumps(_comment), encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.02)


@_algorithm
def open_wpv_2901(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # msg_comment = bytes(json.dumps({"step": "2901", "service_id": "", "params": ""}),
    #                     encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def close_wpv_2902(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # _comment = {"step": "2902", "service_id": "", }
    # msg_comment = bytes(json.dumps(_comment), encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.02)


@_algorithm
def open_pip_1301(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # msg_comment = bytes(json.dumps({"step": "1301", "service_id": "",
    #                                 "params": json.dumps({"vehicle_type": "ES6",
    #                                                       "is_unmanned_station": "1",
    #                                                       "station_type": "2"})}),
    #                     encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def close_pip_1302(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # _comment = {"step": "1302", "service_id": "", }
    # msg_comment = bytes(json.dumps(_comment), encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def open_bbsa_1001(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.8)


@_algorithm
def close_bbsa_1002(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # _comment = {"step": "1002", "service_id": "", }
    # msg_comment = bytes(json.dumps(_comment), encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def open_bsa_1101(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def close_bsa_1102(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    # msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    # _comment = {"step": "1102", "service_id": "", }
    # msg_comment = bytes(json.dumps(_comment), encoding='utf-8')
    # _data = [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]
    # send_topic_data(lock, pub_socket, _data)
    time.sleep(0.2)


@_algorithm
def open_bscc_1201(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def close_bscc_1202(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def open_rsdv_vlsv2_1601(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def close_rsdv_vlsv2_1602(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)

@_algorithm
def open_smd_1701(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def close_smd_1702(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)

@_algorithm
def open_vor_2301(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def close_vor_2302(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def open_wlcc_2501(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def close_wlcc_2502(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def open_sapa_2701(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def close_sapa_2702(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def open_bbcc_2801(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def close_bbcc_2802(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.2)


@_algorithm
def open_lsd_3101(lock, pub_socket, data, param, *args, **kwargs):
    """

    :param lock:
    :param pub_socket:
    :param data:
    :param param:
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.02)