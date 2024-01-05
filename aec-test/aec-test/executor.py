"""
@Author: wenlong.jin
@File: executor.py
@Project: aec-test
@Time: 2023/7/7 11:28
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time
import requests
import json
import threading
from datetime import datetime
from threading import Lock
from multiprocessing import Pipe, Process, Queue

import zmq
import case as case_module

from utils import log, check_ip_address_available, generate_report_data
from command import ExecutorException

_aec_ip = "tcp://192.168.1.13:8800"
_mcs_ip = "tcp://192.168.1.10:8800"
result_url = "https://pangea.nioint.com/pangea/v1/sub-system/finish/recall"


def receive(out_pipe, in_pipe, q, ):
    """
    接收AEC的返回数据，并进行打印，暂不处理
    :param out_pipe:
    :param in_pipe:
    :param q:
    :return:
    """
    out_pipe.close()
    topic = b"AEC"
    context = zmq.Context()
    log.debug(f"<MCS>:Connecting `{_aec_ip}` server…")
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(_aec_ip)
    sub_socket.subscribe(topic)
    while True:
        if not q.empty():
            in_pipe.send("end")
            sub_socket.close()
            break
        rec = sub_socket.recv_multipart()
        systime = int(time.time() * 1000)
        _topic = rec[0].decode()  # MCS
        _timestamp = int(rec[1].decode())
        _type = rec[2].decode()  # b"HB"
        _command = rec[3].decode()  #
        try:
            if rec[4]:
                _comment = json.loads(rec[4])  #
            else:
                log.warning(f"{_topic}, {_type}, {rec[4]}")
                continue
        except Exception as e:
            log.warning(f"{_topic}, {_type}, {rec[4]}")
            raise e
        # print(_comment, type(_comment))
        if _type == "HB":
            in_pipe.send({
                "command": _type,
                "timestamp": _timestamp,
                "comment": _comment
            })
            # log.debug(
            #     f"<MCS>:recv systime:{systime} msg timestamp:{_timestamp}, topic:{_topic}, type:{_type}, command:{_command}, comment:{_comment.decode()}")
            continue
        elif _type == "INFO":
            if _command == "AI-MODEL-VERSION":
                continue
            else:
                in_pipe.send({
                    "command": _command,
                    "timestamp": _timestamp,
                    "comment": _comment
                })
            log.debug(
                f"<MCS>:recv systime:{systime} msg timestamp:{_timestamp}, topic:{_topic}, type:{_type}, command:{_command}, comment:{_comment}")
    log.debug("<MCS>:receive process end ...")


def send_hb(lock, pub_socket, q):
    """
    MCS 发布心跳信号
    :param pub_socket:
    :return:
    """
    while True:
        try:
            _topic = b"MCS"
            _timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
            _type = b"HB"
            _command = b""
            _comment = b""
            _data = [_topic, _timestamp, _type, _command, _comment]
            with lock:
                if not q.empty():
                    break
                pub_socket.send_multipart(_data)
            time.sleep(1)
        except Exception as e:
            log.error(f"<MCS>: send hb happen error {e}")
            break
    log.info("<MCS>:thread send_hb end...")


def send_station_id(lock, pub_socket, q):
    """
    MCS send 站ID
    :param pub_socket:
    :return:
    """
    while True:
        try:
            _topic = b"MCS"
            _timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
            _type = b"INFO"
            _command = b"SWAP-ID"
            _comment = b"PS-NIO-ad1100b5-98123ce6"
            _data = [_topic, _timestamp, _type, _command, _comment]
            with lock:
                if not q.empty():
                    break
                pub_socket.send_multipart(_data)
            time.sleep(0.5)
        except Exception as e:
            log.error(f"<MCS>: send station id request happen error {e}")
            break
    log.info("<MCS>:thread send_station_id end...")


def update_ctrl_data(out_pipe, detail):
    """
    接收到AEC发送的数据，更新MCS发送的数据
    :param out_pipe:
    :param detail
    :return:
    """
    while True:
        content = out_pipe.recv()
        if isinstance(content, str):
            break
        command = content.get("command")
        detail[command] = content
    log.info("<MCS>:thread update_ctrl_data end ...")


def send(resource, out_pipe, in_pipe, q):
    """
    MCS 发布
    :param resource:
    :param out_pipe:进程间通信
    :param in_pipe:
    :param q:进程间通信，用于终止进程
    :return:
    """
    context = zmq.Context()
    pub_socket = context.socket(zmq.PUB)
    pub_socket.setsockopt(zmq.LINGER, 0)
    pub_socket.bind(_mcs_ip)
    log.debug(f"<MCS>:MCS bind `{_mcs_ip}`, rec script data and send to `{_aec_ip}`")
    in_pipe.close()
    detail = {}
    lock = Lock()
    threads = [threading.Thread(target=send_hb, name="send_hb", args=(lock, pub_socket, q)),
               threading.Thread(target=send_station_id, name="send_station_id", args=(lock, pub_socket, q)),
               threading.Thread(target=update_ctrl_data, name="update_ctrl_data", args=(out_pipe, detail)),
               ]
    for th in threads:
        th.daemon = True
        th.start()
    time.sleep(20)
    executor_case(resource, q, lock, pub_socket, detail)
    # pub_socket.close()
    log.debug("<MCS>:send process end....")


def send_case_result_pangea(test_id, result):
    """

    :param test_id:
    :param result:
    :return:
    """
    try:
        data = {"test_id": test_id,
                "test_case_id": result["case_name"],
                "success": result["PASS"],
                "failure": result["TOTAL"] - result["PASS"],
                "detail": ""}
        if result["message"]:
            data["detail"] = result["message"]
        else:
            tmp_str = ""
            for num, num_data in result["detail"].items():
                tmp_str += f"num:{num},{num_data['data']};"
            data["detail"] = tmp_str[:100]  # 避免字符串过长
        response = requests.post(result_url, json=data)
        if response.status_code != 200:
            log.error(f"<MCS>:post pangea response error, status_code:{response.status_code}, reason:{response.reason}")
        else:
            log.info(f"<MCS>:{result['case_name']} result data post pangea success")
    except Exception as e:
        log.error(f"<MCS>:post pangea result data happen error, {e}")


def executor_case(resource, q, lock, pub_socket, detail):
    """

    :param resource:
    :param q:
    :param lock:
    :param pub_socket:
    :param detail:
    :return:
    """
    res = {
        "start": int(time.time() * 1000),
        "data": []
    }
    test_id = resource.get("test_id")
    test_detail = resource.get("test_detail", [])
    params = resource.get("aec_version", {})  # 用于后续判断是执行2代站还是三代站case
    for case in test_detail:
        test_case_id = case.get("test_case_id")
        test_count = int(case.get("test_count"))
        if not test_case_id or test_count < 0:
            log.warning(f"<AEC> case {test_case_id} test number is {test_count}")
            continue
        result = {}
        result["case_name"] = test_case_id
        result["start_time"] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        result["end_time"] = ""
        result["result"] = ""
        result["TOTAL"] = test_count
        result["PASS"] = 0
        result["FAIL"] = 0
        result["NT"] = test_count
        result["message"] = ""
        result["detail"] = {}
        try:
            case = getattr(case_module, test_case_id)
            delay = 30 if "SwapBattery" in case.__name__ else 5
            for i in range(test_count):
                log.info(f"CASE {case.__name__} begin {i + 1} times")
                data = {}
                data["num"] = i + 1
                data["start_time"] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                data["end_time"] = ""
                data["result"] = "PASS"
                data["data"] = []
                case(lock, pub_socket, data, detail, params=params)
                data.pop("num")
                if data["result"] == "PASS":
                    result["PASS"] += 1
                else:
                    result["FAIL"] += 1
                result["NT"] -= 1
                time.sleep(delay)
                data["data"] = ", ".join(data["data"])
                data["end_time"] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                result["detail"][i + 1] = data
                log.info(f"CASE {case.__name__} end {i + 1} times")
            log.info(f"CASE {case.__name__} end all ...")
            # pub_socket.close()
        except TypeError:
            log.error(f"Send Process check: {case} not in case_module, happen type error")
            result["message"] = f"Send Process:{case} not in case_module, parameters not correct..."
        except AttributeError:
            log.error(f"Send Process check: {case} not in case_module.....")
            result["message"] = f"Send Process:{case} not in case_module, parameters not correct..."
            break
        except KeyboardInterrupt:
            log.error("Send Process ctrl + c manual stop process.....")
            result["message"] = "Send Process:ctrl + c manual stop process..."
            break
        except Exception as e:
            log.error(str(e) + "......")
            result["message"] = f"{str(e)}" + "......"
            result["end_time"] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        result["end_time"] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        result["result"] = "PASS" if result["TOTAL"] == result["PASS"] else "FAIL"
        res["data"].append(result)
        if __name__ != "__main__":
            send_case_result_pangea(test_id, result)
    log.info(res)
    q.put(res)
    time.sleep(5)
    log.debug("<MCS>:begin generate_report_data...")
    generate_report_data(res)


def mcs_init_process(resource, ):
    """

    :param case
    :return:
    """
    try:
        if not check_ip_address_available():
            raise ExecutorException("hardware env happen error, 192.168.1.10:8080 can not be used")
        procs = {}
        q = Queue()
        out_pipe, in_pipe = Pipe()  # 用于脚本和数据更新监听使用
        procs["receive"] = Process(target=receive, args=(out_pipe, in_pipe, q))
        procs["send"] = Process(target=send, args=(resource, out_pipe, in_pipe, q,))
        procs["receive"].daemon = True
        procs["receive"].start()
        procs["send"].daemon = True
        procs["send"].start()
        log.debug(f"<MCS>:MCS sub process receive {procs['receive'].pid}, send {procs['send'].pid}")
        procs["receive"].join()
        time.sleep(10)
        log.debug(f"<MCS: MCS sub process send alive is {procs['send'].is_alive()}")
        # for name, proc in procs.items():
        #     proc.join()
        #     log.debug(f"<MCS>:--->>>{name} process end<<<---")
        log.debug("<MCS>: aw executor end ... ")
    except KeyboardInterrupt:
        log.error("Main Process ctrl + c manual stop process")
    except ExecutorException as e:
        log.error(str(e))
    except Exception as e:
        log.error((str(e)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("define test swap number")
    parser.add_argument('--case', action='append', default=[], help='test case name')
    parser.add_argument('--num', action='append', default=[], help='test swap charge number')
    parser.add_argument('--ver', default=3, help='default aec version')
    args = parser.parse_args()
    _resource = {"test_id": "111", "test_detail": [], "aec_version": {"version": args.ver}}
    for i in range(len(args.case)):
        test_count = int(args.num[i]) if len(args.num) >= len(args.case) else 1
        res = {"test_case_id": args.case[i], "test_count": test_count}
        _resource["test_detail"].append(res)
    mcs_init_process(_resource)
