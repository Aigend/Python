"""
@Author: wenlong.jin
@File: aec_utils.py
@Project: ps30
@Time: 2023/7/25 14:06
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import json
import threading
import time
from datetime import datetime
from multiprocessing import Process

import zmq

from aec import *

ai_threading = {}

cmd_map = {
    "1001": "AEC-BBSA",
    "1101": "AEC-BSA",
    "1401": "AEC-PPP",
    "1301": "AEC-PiP",
    "2601": "AEC-RSDS",
    "1501": "AEC-RSDV_PiP",
    "2201": "AEC-ViP",
    "2401": "AEC-WL",
    "2901": "AEC-WPV",
}


def recursion_set(status, data, module=""):
    if isinstance(data, dict):
        for k, v in status.items():
            if k in data and isinstance(v, (str, int,)):
                if isinstance(v, int) and isinstance(data.get(k), str) and data.get(k).isnumeric():
                    status[k] = int(data.get(k))
                elif isinstance(v, str) and isinstance(data.get(k), str):
                    status[k] = data.get(k)
                elif isinstance(v, float) and isinstance(data.get(k), str):
                    try:
                        t = float(data.get(k))
                        status[k] = t
                    except ValueError:
                        loger.error(f"<AEC>:{module}, {k} script data type not match ")
                else:
                    loger.warning(f"<AEC>:{module}, {k} data type not match with script data")
            elif k in data and isinstance(v, dict):
                recursion_set(status[k], data[k], module)


def threading_algorithm(delay=1):
    """
    更新算法的运行状态，并返回对应算法的返回值
    :param delay:
    :return:
    """

    def decorate(func):
        def _run(f, data, in_pipe, flag, step, delay):
            loger.info(f"<AEC>:{f.__name__}, start and update status...")
            in_pipe.send({cmd_map.get(step): 1})  # 更新已启动
            while True:
                f(data, in_pipe)  # 运行对应的算法
                if not flag.get(step):  # 检查是否要停止算法
                    loger.info(f"<AEC>:{f.__name__}, ending and update status...")
                    in_pipe.send({cmd_map.get(step): 0})
                    break
                time.sleep(delay)  # 这个时间根据具体的算法允许时间调整
            # loger.warning(f"<AEC>:threading func {f.__name__} end...")

        @functools.wraps(func)
        def wrapper(data, in_pipe, flag, step, delay=1):
            if (step not in ai_threading or not ai_threading[step].is_alive()) and flag.get(step):
                th = threading.Thread(target=_run, args=(func, data, in_pipe, flag, step, delay))
                th.daemon = True
                th.start()
                ai_threading[step] = th
                time.sleep(0.02)
                loger.info(
                    f'<AEC><RECEIVE>:algorithm {step} threading begin starting, status {ai_threading[step].is_alive()}')

        return wrapper

    return decorate


def single_algorithm(func):
    """
    该函数的目的是用于更新只需要运行1次的算法运行状态
    算法运行1次，但是AEC心跳的算法状态是一直配置运行
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(data, in_pipe, flag, step):
        if flag.get(step):
            # loger.warning(f"<AEC>:send func {func.__name__}, start flag to pipe to update status...")
            in_pipe.send({cmd_map.get(step): 1})  # 更新已启动
            return func(data, in_pipe)
        # loger.warning(f"<AEC>:send func {func.__name__}, end flag to pipe to update status...")
        in_pipe.send({cmd_map.get(step): 0})  # 更新已关闭

    return wrapper


# @single_algorithm
def create_bbsa(data, *args):
    """
    <BBSA>电池下表面拍照
        [2023-06-13 09:50:10.349454] [PS-NIO-5b184b01-b394efc9] [2862] <Info> <AI>
        recv type[INFO] cmd[AEC-BBSA] body[
        {"result":1,"error_code":0,"reason":"{\"timestamp\":\"1686621008196\",
        \"img_name\":\"PS-NIO-5b184b01-b394efc9be4061701733439ea8e17f1906d915ef1686620993084__ds2_f.jpg\",
        \"img_transfer_state\":0,\"battery_type\":2}"}]
    :param data:
    :param args:
    :return:
    """
    msg_topic = b"AEC"
    msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    msg_type = b"INFO"
    msg_command = b"AEC-BBSA"
    status = {
        "result": 0,  # 0/1/-1,   0:电池下表面拍照并发送成功， 1:电池下表面拍照发送不成功， -1 信息不可用或 AEC执行遇到错误
        "error_code": 0,
        "reason": {
            "timestamp": msg_timestamp.decode(),
            "img_name": "",
            "img_transfer_state": 0,  # //0 发送失败， 1 发送成功
            "battery_type": 0  # //1 服务电池， 2 亏电电池，255电池类型未知
        },
    }
    cache_data = data.get("bbsa", {})
    recursion_set(status, cache_data, "bbsa")
    status["reason"] = json.dumps(status["reason"])
    msg_comment = json.dumps(status).encode(encoding='utf-8')
    return [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]


# @single_algorithm
def create_bsa(data, *args):
    """
    <BSA> 电池上表面异物检查
    [2023-06-13 09:51:38.309486] [PS-NIO-5b184b01-b394efc9] [2862]
    <Info> <AI> recv type[INFO] cmd[AEC-BSA] body[
            {"result":0,"error_code":0,"reason":"","detail":
            "{\"result\":0,
            \"timestamp\":\"1686621096156\",
            \"origin_img_name\":\"PS-NIO-5b184b01-b394efc9be4061701733439ea8e17f1906d915ef1686620993084__us1.jpg\",
            \"origin_img_transfer_state\":0,
            \"failure_img_name\":\"\",
            \"failure_img_transfer_state\":0,
            \"battery_type\":1}",
            "mode":"active"}]
    :param data:
    :param args:
    :return:
    """
    msg_topic = b"AEC"
    msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    msg_type = b"INFO"
    msg_command = b"AEC-BSA"
    msg_timestamp.decode()
    status = {
        "result": 0,  # 0/1/-1,, 0没有异物， 1 有异物， -1 信息不可用或 AEC执行遇到错误
        "error_code": 0,
        "reason": "",
        "detail": {
            "result": 0,
            "timestamp": 0,
            "origin_img_name": "",
            "origin_img_transfer_state": 0,
            "failure_img_name": "",
            "failure_img_transfer_state": 0,
            "battery_type": 0
        },
        "mode": ""  # active: 正常模式   shadow: 影子模式
    }
    cache_data = data.get("bsa", {})
    recursion_set(status, cache_data, "bsa")
    status["detail"] = json.dumps(status["detail"])
    msg_comment = json.dumps(status).encode(encoding='utf-8')
    return [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]


# def create_bscc(data, in_pipe, *args):
#     """
#     <BSCC> 电池上表面摄像头检查
#     :param data:
#     :param in_pipe:
#     :param args:
#     :return:
#     """
#     msg_topic = b"AEC"
#     msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
#     msg_type = b"INFO"
#     msg_command = b"BATTERY-SURFACE-CAMERA-CHECK"
#     status = {
#         "result": 0,  # 0/1/-1,, 0摄像头安装好， 1 表示摄像头没有安装好， -1 信息不可用或 AEC执行遇到错误
#         "error_code": 0,
#         "reason": "",
#     }
#     cache_data = data.get("bscc", {})
#     for k, v in status.items():
#         if k in cache_data.keys():
#             status[k] = cache_data.get(k)
#     msg_comment = json.dumps(status).encode(encoding='utf-8')
#     in_pipe.send([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])


# @threading_algorithm(delay=0.5)
def create_pip(data, *args):
    """
     <PiP>人体识别信号
        [2023-06-13 09:52:37.221742] [PS-NIO-5b184b01-b394efc9] [2862] <Info> <AI>
        recv type[INFO] cmd[AEC-PiP] body[
            {"result":0,
            "error_code":0,
            "reason":"",
            "detail":
                "{\"res\":0,
                \"timestamp\":\"20230613095235066\"}",
            "mode":"active"}]
    :param data:
    :param args:
    :return:
    """
    msg_topic = b"AEC"
    msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    msg_type = b"INFO"
    msg_command = b"AEC-PiP"
    status = {
        "result": 0,  # 1/0/-1, # 1 有人 #0 无人 #-1 算法模块无法运行
        "error_code": 0,
        "reason": "",
        "detail": {"res": 0, "timestamp": msg_timestamp.decode()},
        "mode": ""
    }
    cache_data = data.get("pip", {})
    recursion_set(status, cache_data, "pip")
    status["detail"] = json.dumps(status["detail"])
    msg_comment = json.dumps(status).encode(encoding='utf-8')
    return [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]


# @threading_algorithm(delay=0.5)
def create_ppp(data, *args):
    """
    <PPP> 倒车入换电站行人检测
    [2023-06-13 09:47:31.969805] [PS-NIO-5b184b01-b394efc9] [2862] <Info> <AI>
    recv type[INFO] cmd[AEC-PPP] body[
        {"result":0,
        "error_code":0,
        "reason":"{\"res\":0,\"timestamp\":\"1686620849813\",\"detail\":\"\"}",
        "mode":"active"}]
    :param data:
    :param args:
    :return:
    """
    msg_topic = b"AEC"
    msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    msg_type = b"INFO"
    msg_command = b"AEC-PPP"
    status = {
        "result": 0,  # 0/1/-1,,  0表示没有行人， 1 表示有行人， -1 信息不可用， AEC执行遇到错误
        "error_code": 0,
        "reason": {
            "res": 0,
            "timestamp": msg_timestamp.decode(),
            "detail": ""},
        "mode": ""
    }
    cache_data = data.get("ppp", {})
    recursion_set(status, cache_data, "ppp")
    status["reason"] = json.dumps(status["reason"])
    msg_comment = json.dumps(status).encode(encoding='utf-8')
    return [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]


# @threading_algorithm(delay=0.5)
def create_rsdv_pip(data, *args):
    """
    <AI> recv type[INFO] cmd[AEC-RSDV_PiP]body[
        {
            "result":0,
            "error_code":0,
            "reason":
                "{\"res\":0,\"timestamp\":\"20230425110056088\"}",
            "mode":"active"
        }
    ]
    <RSDV_PiP>卷帘门下降时人体识别
    :param data:
    :param args:
    :return:
    """
    msg_topic = b"AEC"
    msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    msg_type = b"INFO"
    msg_command = b"AEC-RSDV_PiP"
    status = {
        "result": 0,  # 1/0/-1, # 1 有人 #0 无人 #-1 算法模块无法运行
        "error_code": 0,
        "reason": {
            "res": 0,
            "timestamp": datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]},
        "mode": ''
    }
    cache_data = data.get("rsdv_pip", {})
    recursion_set(status, cache_data, "rsdv_pip")
    status["reason"] = json.dumps(status["reason"])
    msg_comment = json.dumps(status).encode(encoding='utf-8')
    return [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]


# @threading_algorithm
# def create_rsdv_vlsv2(data, in_pipe, *args):
#     """
#     （RSDV_VLSV2）卷帘门下降时车辆识别
#     :param data:
#     :param in_pipe:
#     :param args:
#     :return:
#     """
#     pass


# def create_smd(data, in_pipe, *args):
#     """
#     <SMD> 车辆解锁套筒丢失信号
#
#     :param data:
#     :param in_pipe:
#     :param args:
#     :return:
#     """
#     msg_topic = b"AEC"
#     msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
#     msg_type = b"INFO"
#     msg_command = b"SCREW-SOCKET-MISSING"
#     status = {
#         "result": 0,  # 正整数（uint16）/0/-1,  #正整数（uint16） 套筒有掉落 #0 没有套筒丢失#-1 算法模块无法运行
#         # result：正整数， 按位与，得到枪头位置，如0x0005 = 0000 0000 0000 0101， 第一个枪头和第三个枪头掉落。
#         "error_code": 0,
#         "reason": "",
#     }
#     cache_data = data.get("smd", {})
#     for k, v in status.items():
#         if k in cache_data.keys():
#             status[k] = cache_data.get(k)
#     msg_comment = json.dumps(status).encode(encoding='utf-8')
#     in_pipe.send([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])


# def create_vasf(data, in_pipe, *args):
#     """
#     （VASF）车在站前识别
#     :param data:
#     :param in_pipe:
#     :param args:
#     :return:
#     """
#     pass


# def create_vbcc(data, in_pipe, *args):
#     """
#     （VBCC）
#     :param data:
#     :param in_pipe:
#     :param args:
#     :return:
#     """
#     pass


# def create_vbsl(data, in_pipe, *args):
#     """
#     <VBSL> 车身定位
#     :param data:
#     :param in_pipe:
#     :param args:
#     :return:
#     """
#     msg_topic = b"AEC"
#     msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
#     msg_type = b"INFO"
#     msg_command = b"VBSL"
#     status = {
#         "result": 0,  # 正整数（uint32）0/1/-1/-2/-3,  0（正常） 1（车身定位偏差过大） -1（车身定位相机通信断开）-2（车身定位相机图像检测圆错误）-3（车身定位未校准）
#         "error_code": 0,
#         "detail": {
#             "rf_x": "",  # //右前方x轴位置
#             "rf_y": "",  # //右前方y轴位置
#             "rf_img": "",  # //右前方原始照片
#             "rf_out_img": "",  # //右前方处理后照片
#             "timestamp": msg_timestamp  # //时间戳
#         }
#     }
#     cache_data = data.get("vbsl", {})
#     for k, v in status.items():
#         if k in cache_data.keys():
#             status[k] = cache_data.get(k)
#     msg_comment = json.dumps(status).encode(encoding='utf-8')
#     in_pipe.send([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])


# @threading_algorithm(delay=0.5)
def create_vip(data, *args):
    """
    {
        "result": 1,  # 1/0/-1,  1 有车辆 #0 无车辆 #-1 算法模块无法运行(如摄像头掉线、算法加载失败等)
        "error_code": 0,
        "reason": "",
        "detail": {
            "result": 1,
            "res1": 1.1020499179730438e-22,
            "res2": 1,
            "threshold": 0.9,
            "timestamp": 1682390496605
        }
    }
    车辆识别
    (ViP2)
    :param data:
    :param args:
    :return:
    """
    msg_topic = b"AEC"
    msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    msg_type = b"INFO"
    msg_command = b"AEC-ViP"
    status = {
        "result": 0,  # 1/0/-1,  1 有车辆 #0 无车辆 #-1 算法模块无法运行(如摄像头掉线、算法加载失败等)
        "error_code": 0,
        "reason": "",
        "detail": {
            "result": 0,
            "res1": 0.0,
            "res2": 0,
            "threshold": 0.0,
            "timestamp": msg_timestamp.decode()
        }
    }
    cache_data = data.get("vip", {})
    recursion_set(status, cache_data, "vip")
    status["detail"] = json.dumps(status["detail"])
    msg_comment = json.dumps(status).encode(encoding='utf-8')
    return [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]


# def create_vor(data, in_pipe, *args):
#     """
#     <VOR> 车辆进站方向识别
#     :param data:
#     :param in_pipe:
#     :param args:
#     :return:
#     """
#     msg_topic = b"AEC"
#     msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
#     msg_type = b"INFO"
#     msg_command = b"VOR"
#     status = {
#         "result": 0,  # 正整数（uint32）/0/1,  0（正常） #1（有异常）
#         "error_code": 0,
#         "reason": {},
#     }
#     cache_data = data.get("vor", {})
#     for k, v in status.items():
#         if k in cache_data.keys():
#             status[k] = cache_data.get(k)
#     msg_comment = json.dumps(status).encode(encoding='utf-8')
#     in_pipe.send([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])


# @threading_algorithm(delay=0.5)
def create_wl(data, *args):
    """
        <WL> 车轮定位信号
    [2023-06-13 09:47:32.054012] [PS-NIO-5b184b01-b394efc9] [2862] <Info> <AI> recv type[INFO] cmd[AEC-WL] body[
    {"result":2,"error_code":0,"reason":"","detail":
            "{\"res1\":0.99999964237213135,
                \"res2\":3.3635873819548578e-07,
                \"res3\":8.4504403474738865e-09,
                \"threshold\":0.1,
                \"timestamp\":\"1686620849898\"}"}]
    :param data:
    :param args:
    :return:
    """
    msg_topic = b"AEC"
    msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    msg_type = b"INFO"
    msg_command = b"AEC-WL"
    status = {
        "result": 0,  # 1/0/-1,  # 1 车轮在位 #0 车轮不在位 #-1 算法模块无法运行
        "error_code": 0,
        "reason": "0",
        "detail": {
            "res1": 0.0,
            "res2": 0.0,
            "res3": 0.0,
            "threshold": 0.0,
            "timestamp": msg_timestamp.decode(),
        }
    }
    cache_data = data.get("wl", {})
    recursion_set(status, cache_data, "wl")
    status["detail"] = json.dumps(status["detail"])
    msg_comment = json.dumps(status).encode(encoding='utf-8')
    return [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]


# def create_wlcc(data, in_pipe, *args):
#     """
#     <WLCC> 车轮定位摄像头检查
#     :param data:
#     :param in_pipe:
#     :param args:
#     :return:
#     """
#     msg_topic = b"AEC"
#     msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
#     msg_type = b"INFO"
#     msg_command = b"WHEEL-LOCATE-CAMERA-CHECK"
#     status = {
#         "result": 0,  # 0/1/-1,, 0摄像头安装好， 1 表示摄像头没有安装好， -1 信息不可用或 AEC执行遇到错误
#         "error_code": 0,
#         "reason": "",
#     }
#     cache_data = data.get("wlcc", {})
#     for k, v in status.items():
#         if k in cache_data.keys():
#             status[k] = cache_data.get(k)
#     msg_comment = json.dumps(status).encode(encoding='utf-8')
#     in_pipe.send([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])


# @threading_algorithm(delay=0.5)
def create_rsds(data, *args):
    """
    <AI> recv type[INFO] cmd[AEC-RSDS] body[
        {
            "result":0,
            "error_code":0,
            "reason":"",
            "detail":
                "{\"front_up_state\":1,
                \"front_down_state\":1,
                \"back_up_state\":1,
                \"back_down_state\":1,
                \"timestamp\":\"1682391657740\"}",
            "mode":"active"
        }
    ]
    <RSDS> 卷帘门状态
    :param data:
    :param args:
    :return:
    """
    msg_topic = b"AEC"
    msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    msg_type = b"INFO"
    msg_command = b"AEC-RSDS"
    status = {
        "result": 0,  # 正整数（int32）/0/-1,  0（结果可用），-1（结果不可用，有异常，异常参见error_code字段）
        "error_code": 0,
        "reason": "",
        "detail": {
            "front_up_state": 0,  # (0：触发[检测到目标] 1：未触发[未检测到目标] 2: 未知)
            "front_down_state": 0,  # (0：触发[检测到目标] 1：未触发[未检测到目标] 2: 未知)
            "back_up_state": 0,  # (0：触发[检测到目标] 1：未触发[未检测到目标] 2: 未知)
            "back_down_state": 0,  # (0：触发[检测到目标] 1：未触发[未检测到目标] 2: 未知)
            "timestamp": msg_timestamp.decode()
        },
        "mode": ""
    }
    cache_data = data.get("rsds", {})
    recursion_set(status, cache_data, "rsds")
    status["detail"] = json.dumps(status["detail"])
    msg_comment = json.dumps(status).encode(encoding='utf-8')
    return [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]


# @threading_algorithm
# def create_sapa(data, in_pipe, *args):
#     """
#     <SAPA> 安全自动泊车预警
#     :param data:
#     :param in_pipe:
#     :param args:
#     :return:
#     """
#     msg_topic = b"AEC"
#     msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
#     msg_type = b"INFO"
#     msg_command = b"SAPA"
#     status = {
#         "result": 0,  # /0/1,  0（正常） #1（有告警）
#         "error_code": 0,
#         "reason": {},
#     }
#     cache_data = data.get("sapa", {})
#     for k, v in status.items():
#         if k in cache_data.keys():
#             status[k] = cache_data.get(k)
#     msg_comment = json.dumps(status).encode(encoding='utf-8')
#     in_pipe.send([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])


# def create_bbcc(data, in_pipe, *args):
#     """
#     枪头掉落安装位置检测 (BBCC)
#     :param data:
#     :param in_pipe:
#     :param args:
#     :return:
#     """
#     pass


# @single_algorithm
def create_wpv(data, *args):
    """
    <WPV> 车身整体倾斜定位（压推杆识别）
    [2023-06-13 09:48:35.015133] [PS-NIO-5b184b01-b394efc9] [2862] <Info> <AI>
    recv type[INFO] cmd[AEC-WPV] body[
    {"result":0,"error_code":0,"reason":"",
    "detail":"{\"lf\":0,\"rf\":0,\"lb\":0,\"rb\":0}","mode":"active"}]
    :param data:
    :param args:
    :return:
    """
    msg_topic = b"AEC"
    msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
    msg_type = b"INFO"
    msg_command = b"AEC-WPV"
    status = {
        "result": 0,  # 正整数（uint32）/0/1/-1,  #0（正常）1（压推杆）-1（相机掉线）
        "error_code": 0,
        "reason": "",
        "detail": {
            "lf": 0,  # //左前，0（正常）、1（压推杆）
            "rf": 0,  # //右前
            "lb": 0,  # //左后
            "rb": 0,  # //右后
        },
        "mode": ""
    }
    cache_data = data.get("wpv", {})
    recursion_set(status, cache_data, "wpv")
    status["detail"] = json.dumps(status["detail"])
    msg_comment = json.dumps(status).encode(encoding='utf-8')
    return [msg_topic, msg_timestamp, msg_type, msg_command, msg_comment]


# def create_rc(data, in_pipe, *args):
#     """
#     <RC> 参数更新
#     :param data:
#     :param in_pipe:
#     :return:
#     """
#     msg_topic = b"AEC"
#     msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
#     msg_type = b"INFO"
#     msg_command = b"RC"
#     status = {
#         "result": 0,  # 0 更新成功 #1 更新失败
#     }
#     cache_data = data.get("rc", {})
#     for k, v in status.items():
#         if k in cache_data.keys():
#             status[k] = cache_data.get(k)
#     msg_comment = json.dumps(status).encode(encoding='utf-8')
#     in_pipe.send([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])


algorithm_map = {
    "bbsa": create_bbsa,  # <BBSA>电池下表面拍照, 单次
    "bsa": create_bsa,  # <BSA> 电池上表面异物检查, 单次
    # "1201": create_bscc,  # <BSCC> 电池上表面摄像头检查, 单次
    "pip": create_pip,  # <PiP>人体识别信号，启动
    # "1302": create_pip,
    "ppp": create_ppp,  # <PPP> 倒车入换电站行人检测
    # "1402": create_ppp,
    "rsdv_pip": create_rsdv_pip,  # <RSDV_PiP>卷帘门下降时人体识别
    # "1502": create_rsdv_pip,
    # "1601": create_rsdv_vlsv2,  # （RSDV_VLSV2）卷帘门下降时车辆识别
    # "1602": create_rsdv_vlsv2,
    # "1701": create_smd,  # <SMD> 车辆解锁套筒丢失信号
    # "2001": create_vbsl,  # <VBSL>
    "vip": create_vip,  # <ViP2> 车辆识别
    # "2202": create_vip2,
    # "2301": create_vor,  # <VOR> 车辆进站方向识别
    "wl": create_wl,  # <WL> 车轮定位信号
    # "2402": create_wl,
    # "2501": create_wlcc,  # <WLCC> 车轮定位摄像头检查
    "rsds": create_rsds,  # <RSDS> 卷帘门状态
    # "2602": create_rsds,
    # "2701": create_sapa,  # <SAPA> 安全自动泊车预警
    # "2702": create_sapa,
    # "2801": create_bbcc,  # 枪头掉落安装位置检测 (BBCC)
    "wpv": create_wpv,  # 车身整体倾斜定位（压推杆识别） (WPV)
}


def receive(receive_q):
    """
        订阅MCS,获取主控下发给AEC的zmq消息
        心跳和待执行的算法步骤号，MCS 回复的站ID 请求
    :return:
    """
    topic = b"MCS"
    context = zmq.Context()
    loger.info(f"<AEC><RECEIVE>:Connecting {mcs_ip} server…")
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(mcs_ip)
    sub_socket.subscribe(topic)
    while True:
        rec = sub_socket.recv_multipart()
        msg_topic = rec[0].decode()
        msg_timestamp = rec[1].decode()
        msg_type = rec[2].decode()  # b"HB", b"INFO"
        msg_command = rec[3].decode()  # b"SWAP_ID"
        msg_comment = rec[4].decode()  # b"PS-NIO-ad1100b5-98123ce6"
        if msg_command == "STEP":
            msg_comment = json.loads(msg_comment)
            msg_comment_cmd = msg_comment["step"]
            if  msg_comment_cmd != "0":
                loger.info(f"<AEC><RECEIVE>: {rec}")
                receive_q.put(msg_comment_cmd)

            #loger.info(
                #f"<AEC><RECEIVE>:msg_topic:{msg_topic}, msg_type:{msg_type}, msg_command:{msg_command}, msg_comment:{msg_comment}, #msg_timestamp:{msg_timestamp}")
            # comment = json.loads(msg_comment)
            # step = comment.get("step")
            # if isinstance(step, str) and step.isnumeric():
            #     if step in algorithm_map:
            #         flag[step] = True  # 开启算法
            #     elif not int(step) % 2 and str(int(step) - 1) in algorithm_map:
            #         step = str(int(step) - 1)
            #         flag[step] = False  # 关闭算法
            #     else:
            #         loger.warning(f"<AEC><RECEIVE>:step {step} not support")
            #         continue
            #     algorithm_map.get(step)(data, in_pipe, flag, step)  # 存在的算法就进行调用


def create_HB(pub_socket, data):
    """
    AEC 发布心跳信号
    :param pub_socket:
    :param data:
    :return:
    """
    msg_topic = b"AEC"
    msg_type = b"HB"
    msg_command = b""
    status = {
        "camera_1_work_state": 1,
        "camera_2_work_state": 1,
        "camera_3_work_state": 1,
        "camera_4_work_state": 1,
        "camera_5_work_state": 1,
        "camera_6_work_state": 1,
        "camera_7_work_state": 1,
        "camera_9_work_state": 1,
        "AEC-BBSA": 0,  # //0表示不运行 1表示运行中
        "AEC-BSA": 0,  # //0表示不运行 1表示运行中
        "AEC-PPP": 0,  # //0表示不运行 1表示运行中
        "AEC-PiP": 0,  # //0表示不运行 1表示运行中
        "AEC-RSDS": 0,  # //0表示不运行 1表示运行中
        "AEC-RSDV_PiP": 0,  # //0表示不运行 1表示运行中
        "AEC-ViP": 0,  # //0表示不运行 1表示运行中
        "AEC-WL": 0,  # //0表示不运行 1表示运行中
        "AEC-WPV": 0,  # //0表示不运行 1表示运行中
        "version": "",  # "023012.1.5.2"
    }
    while True:
        hb = data.get('hb')
        recursion_set(status, hb, "hb")
        msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
        msg_comment = json.dumps(status).encode(encoding='utf-8')
        pub_socket.send_multipart([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])
        # loger.info([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])
        time.sleep(1)


def create_req_id(pub_socket):
    """
        AEC 请求获取站ID
    :param pub_socket:
    :return:
    """
    msg_topic = b"AEC"
    msg_type = b"INFO"
    msg_command = b"SWAP-ID"
    msg_comment = b""
    while True:
        msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
        pub_socket.send_multipart([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])
        time.sleep(0.5)


def create_ai_model_version(pub_socket, data):
    """

    :param pub_socket:
    :param data
    :return:
    """
    msg_topic = b"AEC"
    msg_type = b"INFO"
    msg_command = b"AI-MODEL-VERSION"
    comment = [{"model": "AEC-BSA3", "version": ""},  # "1.0.1"
               {"model": "AEC-WL3", "version": ""},  # 1.0.3
               {"model": "AEC-ViP3", "version": ""},
               {"model": "AEC-PiP3", "version": ""},
               {"model": "AEC-PPP3", "version": ""},
               {"model": "AEC-RSDS3", "version": ""},
               {"model": "AEC-WPV3", "version": ""}]
    while True:
        msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
        temp = {}
        if data.get("ai-model-version"):
            tmp = data["ai-model-version"]
            if isinstance(tmp, list):
                for vals in tmp:
                    if "version" in vals and "model" in vals:
                        temp[vals['model']] = vals['version']
        for vals in comment:
            vals['version'] = temp.get(vals['model'], '')
        msg_comment = json.dumps(comment).encode(encoding='utf-8')
        pub_socket.send_multipart([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])
        time.sleep(5)


def send(queue,receive_q):
    """

    :return:
    """
    context = zmq.Context()
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind(aec_ip)
    loger.info(f"<AEC><SEND>:AEC bind `{aec_ip}`, rec script data and send to `{mcs_ip}` ...")
    data = {}
    threads = [threading.Thread(target=create_HB, args=(pub_socket, data), name="hb"),
               threading.Thread(target=create_ai_model_version, args=(pub_socket, data), name="ai-model-version"),
               threading.Thread(target=create_req_id, args=(pub_socket,), name="swap_id"), ]
    for th in threads:
        th.daemon = True
        th.start()
    time.sleep(0.05)
    msg_topic = b"AEC"
    msg_type = b"INFO"
    
    while True:
        try:  
            while not receive_q.empty():
                msg_comment_cmd = receive_q.get()
                loger.info(f"<AEC><SEND>=================receive==: {msg_comment_cmd}")
                
                if msg_comment_cmd=="1001":
                    aec_result = {"HB": {"AEC-BBSA": "1", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)                 
                    
                    aec_result =  {"BBSA": {"detail": {"battery_type": "0", "failure_img_name": "xxx", "failure_img_transfer_state": "0", "img_name": "xxx", "img_transfer_state": "0", "origin_img_name": "xxx", "origin_img_transfer_state": "0", "result": "0", "timestamp": "1636956028619"}, "error_code": "0", "mode": "active", "reason": "xxx", "result": "0"}} 
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"bbsa": aec_result}                    
                    queue.put(aec_result_data)                       
                    
                if msg_comment_cmd=="1002": 
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "1", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)                 
                
                if msg_comment_cmd=="1101":
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "1", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)                 
                    
                    aec_result =  {"BSA": {"detail": {"battery_type": "0", "detect_items": [4, 11], "failure_img_name": "xxx", "failure_img_transfer_state": "0", "origin_img_name": "xxx", "origin_img_transfer_state": "0", "result": "0", "timestamp": "1636956028619"}, "error_code": "0", "mode": "active", "reason": "xxx", "result": "0"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"bsa": aec_result}                    
                    queue.put(aec_result_data)                       
                    
                if msg_comment_cmd=="1102": 
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "1", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)      
                    
                if msg_comment_cmd=="1301":                 
                 
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "1", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)                 
                    
                    aec_result =  {"PiP": {"detail": {"res": "0", "timestamp": "1636956028619"}, "error_code": "0", "mode": "active", "reason": "xxx", "result": "0"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"pip": aec_result}                    
                    queue.put(aec_result_data)                 
                
                
                if msg_comment_cmd=="1302": 
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "1", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)  
                if msg_comment_cmd=="1401":                 
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "1", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)                 
                    
                    aec_result =  {"PPP": {"detail": {"detail": "xxx", "res": "0", "timestamp": "1636956028619"}, "error_code": "0", "mode": "active", "reason": "xxx", "result": "0"}}
                    aec_result_data = {"ppp": aec_result}                    
                    queue.put(aec_result_data) 
                
                if msg_comment_cmd=="1402":  
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)     
                
                if msg_comment_cmd=="1501": 
                    loger.info("need to update this cmd")
                if msg_comment_cmd=="1502":  
                    loger.info("need to update this cmd")                
                if msg_comment_cmd=="1601":   
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="1602":  
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="1701":  
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="1702":  
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="1801":  
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="1802":  
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="1901":  
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="1902":   
                    loger.info("need to update this cmd")   
                if msg_comment_cmd=="2001":   
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="2002": 
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="2101":  
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="2102":   
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="2201":     #result=0,车不在平台，=1车在平台
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "1", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "1", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)                 
                    
                    aec_result =  {"ViP": {"detail": {"res1": "1.13", "res2": "1.13", "result": "0", "threshold": "1.13", "timestamp": "1636956028619"}, "error_code": "0", "mode": "active", "reason": "xxx", "result": "0"}}
                    
                    aec_result_data = {"vip": aec_result}                    
                    queue.put(aec_result_data)                 
                if msg_comment_cmd=="2202": 
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data) 
                    
                if msg_comment_cmd=="2301": 
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="2302":                     
                    loger.info("need to update this cmd")   
                if msg_comment_cmd=="2401":
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "1", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)                
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data) 
                    
                    aec_result = {"WL": {"detail": {"res1": "1.13", "res2": "1.13", "res3": "1.13", "threshold": "1.13", "timestamp": "1636956028619"}, "error_code": "0", "mode": "active", "reason": "xxx", "result": "0"}}
                    aec_result = json.dumps(aec_result)                
                    aec_result_data = {"wl": aec_result}                    
                    queue.put(aec_result_data)  
                    
                if msg_comment_cmd=="2402":
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)                
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)
                if msg_comment_cmd=="2501": 
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="2502":
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="2601":
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "1", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)                 
                    
                    aec_result = {"RSDS": {"detail": {"back_down_state": "1", "back_up_state": "1", "front_down_state": "1", "front_up_state": "1", "timestamp": "1636956028619"}, "error_code": "0", "mode": "active", "reason": "xxx", "result": "0"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"rsds": aec_result}                    
                    queue.put(aec_result_data)                       
                    
                if msg_comment_cmd=="2602": 
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "1", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data) 

                if msg_comment_cmd=="2701":      
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "1", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)                 
                    
                    aec_result = {"SAPA": {"detail": {"detail": "xxx", "result": "0", "timestamp": "1636956028619"}, "error_code": "0", "mode": "active", "reason": "xxx", "result": "0"}}
                    aec_result_data = {"sapa": aec_result}                    
                    queue.put(aec_result_data) 

                
                if msg_comment_cmd=="2702": 
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data)                 
                
                
                if msg_comment_cmd=="2801":    
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="2802": 
                    loger.info("need to update this cmd")   
                
                if msg_comment_cmd=="2901":
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "1", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)                
                    aec_result_data = {"hb": aec_result}                    
                    queue.put(aec_result_data) 
                    
                    aec_result = {"WPV": {"detail": {"lb": "0", "lf": "0", "rb": "0", "rf": "0"}, "error_code": "0", "mode": "active", "reason": "xxx", "result": "0"}}
                    aec_result = json.dumps(aec_result)    
                    aec_result_data = {"wpv": aec_result}                    
                    queue.put(aec_result_data)                     
        
                if msg_comment_cmd=="2902": 
                    aec_result = {"HB": {"AEC-BBSA": "0", "AEC-BSA": "0", "AEC-PPP": "0", "AEC-PiP": "0", "AEC-RSDS": "0", "AEC-SAPA": "0", "AEC-ViP": "0", "AEC-WL": "0", "AEC-WPV": "0", "camera_1_work_state": "1", "camera_2_work_state": "1", "camera_3_work_state": "1", "camera_4_work_state": "1", "camera_5_work_state": "1", "camera_6_work_state": "1", "camera_7_work_state": "1", "camera_8_work_state": "1", "camera_9_work_state": "1", "version": "023012.1.6.3"}}
                    aec_result = json.dumps(aec_result)   
                    aec_result_data = {"hb": aec_result}   
                    queue.put(aec_result_data)  
                if msg_comment_cmd=="3001":  
                    loger.info("need to update this cmd")                   
                if msg_comment_cmd=="3002": 
                    loger.info("need to update this cmd")   
                    
                     
            if queue.empty():
                #time.sleep(1)
                continue
            tmp = queue.get()
            
            data.update(tmp)
            loger.info(f"<AEC><SEND>:receive script data {tmp}")
            (typ, d), = tmp.items()
            
            if typ in ['bbsa', 'bsa', 'pip', 'ppp', 'rsdv_pip', 'vip', 'wl', 'rsds', 'wpv']:
                res = algorithm_map.get(typ)(data)
                loger.info(f"<AEC><SEND>:`{res}`")
                pub_socket.send_multipart(res)
                
        except Exception as e:
            loger.warning(f"<AEC><SEND>:send process happen error {str(e)}")
            time.sleep(5)


def aec_init_back_process(procs,receive_q, send_q):
    """

    :param procs
    :param send_q:
    :return:
    """
    rcv = procs.get("receive")
    snd = procs.get("send")
    if not (isinstance(snd, Process) and snd.is_alive() and isinstance(rcv, Process) and rcv.is_alive()):
        procs["receive"] = Process(target=receive, args=(receive_q,))
        procs["send"] = Process(target=send, args=(send_q,receive_q))
        procs["send"].daemon = True
        procs["receive"].daemon = True
        procs["send"].start()
        procs["receive"].start()
        loger.info(f"<AEC>:aec sub process receive {procs['receive'].pid}, send {procs['send'].pid}")
